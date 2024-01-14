from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "golden_reason_validate_correctness_ct" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "reason_ar" TEXT,
    "reason_en" TEXT,
    "reason_ru" TEXT,
    "validatecorrectnessct_id" INT NOT NULL REFERENCES "validate_correctness_ct" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "golden_reason_validate_correctness_ct"."reason_ar" IS 'The reason in Arabic';
COMMENT ON COLUMN "golden_reason_validate_correctness_ct"."reason_en" IS 'The reason in English';
COMMENT ON COLUMN "golden_reason_validate_correctness_ct"."reason_ru" IS 'The reason in Russian';;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "golden_reason_validate_correctness_ct";"""
