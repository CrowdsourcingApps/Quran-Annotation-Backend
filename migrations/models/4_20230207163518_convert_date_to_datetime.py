from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE TIMESTAMPTZ USING "create_date"::TIMESTAMPTZ;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "task" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_t_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;
        ALTER TABLE "validate_correctness_ct_user" ALTER COLUMN "create_date" TYPE DATE USING "create_date"::DATE;"""
