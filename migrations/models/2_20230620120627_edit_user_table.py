from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "is_anonymous" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" ALTER COLUMN "email" DROP NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "hashed_password" DROP NOT NULL;
       """


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" DROP COLUMN "is_anonymous";
        ALTER TABLE "user" ALTER COLUMN "email" SET NOT NULL;
        ALTER TABLE "user" ALTER COLUMN "hashed_password" SET NOT NULL;
        DROP TABLE IF EXISTS "pushnotificationtoken";
        """
