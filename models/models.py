from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, Boolean, ForeignKey

metadata = MetaData()

user = Table(
    "user",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_name", String, nullable=False),
    Column("user_surname", String, nullable=False),
    Column("car_model", String, nullable=False),
    Column("car_brand", String, nullable=False),
    Column("phone_number", String, nullable=False),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
    Column("email", String, nullable=False),
    Column("hashed_password", String, nullable=False),
    Column("is_active", Boolean, default=True, nullable=False),
    Column("is_superuser", Boolean, default=False, nullable=False),
    Column("is_verified", Boolean, default=False, nullable=False),

)
request = Table(
    "request",
    metadata,
    Column("id", Integer, primary_key=True),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("title", String, nullable=False),
    Column("service", String, nullable=False),
    Column("comment", String, nullable=False),
    Column("is_archived", Boolean, default=False),
    Column("date", String),
    Column("registered_at", TIMESTAMP, default=datetime.utcnow()),
)
