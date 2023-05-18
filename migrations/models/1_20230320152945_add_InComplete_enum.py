from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "label" TYPE VARCHAR(17) USING "label"::VARCHAR(17);"""
