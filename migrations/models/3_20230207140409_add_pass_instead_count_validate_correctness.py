from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "validate_correctness_exam_pass" BOOL NOT NULL  DEFAULT False;
        ALTER TABLE "user" DROP COLUMN "validate_correctness_exam_correct_no";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "validate_correctness_exam_correct_no" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "user" DROP COLUMN "validate_correctness_exam_pass";"""
