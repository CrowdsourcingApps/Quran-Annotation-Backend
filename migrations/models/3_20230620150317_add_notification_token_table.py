from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "notificationtoken" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "token" VARCHAR(255) NOT NULL,
    "platform" VARCHAR(50) NOT NULL,
    "update_date" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE
);;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "notificationtoken";"""
