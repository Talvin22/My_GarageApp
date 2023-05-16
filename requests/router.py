from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, insert, delete, update
from sqlalchemy.ext.asyncio import AsyncSession

from auth.database import get_async_session, Request, User
from models.models import request, user
from requests.schemas import RequestCreate, RequestUpdate

router = APIRouter(
    prefix="/requests",
    tags=["Request"]
)


@router.get("/{request_id}")
async def get_request(request_id: int, session: AsyncSession = Depends(get_async_session)):
    query = select(request).where(request.c.user_id == request_id)
    result = await session.execute(query)
    data = list(result.mappings())
    return {"data": data}


@router.post("/")
async def create_request(new_request: RequestCreate, user_id: int, session: AsyncSession = Depends(get_async_session)):
    async with session.begin():
        user = await session.get(User, user_id)
        if user is None:
            raise HTTPException(status_code=404, detail="User not found")

        db_request = Request(**new_request.dict(), user_id=user.id)
        session.add(db_request)
        await session.flush()
        await session.refresh(db_request)
        return db_request


@router.delete("/{request_id}")
async def delete_request(request_id: int, session: AsyncSession = Depends(get_async_session)):
    query = delete(request).where(request.c.id == request_id)
    result = await session.execute(query)
    await session.commit()
    return {"status": "success"}


@router.put("/{request_id}")
async def update_request(request_id: int, updated_request: RequestUpdate,
                         session: AsyncSession = Depends(get_async_session)):
    query = select(request).where(request.c.id == request_id)
    result = await session.execute(query)
    existing_request = result.scalar()

    if not existing_request:
        raise HTTPException(status_code=404, detail="Request not found")

    update_data = updated_request.dict(exclude_unset=True)
    await session.execute(update(request).where(request.c.id == request_id).values(**update_data))
    await session.commit()

    return {"status": "success"}
