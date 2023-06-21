from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(7) USING "platform"::VARCHAR(7);
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(7) USING "platform"::VARCHAR(7);
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(7) USING "platform"::VARCHAR(7);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(50) USING "platform"::VARCHAR(50);
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(50) USING "platform"::VARCHAR(50);
        ALTER TABLE "notificationtoken" ALTER COLUMN "platform" TYPE VARCHAR(50) USING "platform"::VARCHAR(50);"""
