from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "client_id" DROP NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "label" DROP NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "final_transcription" DROP NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "create_date" DROP NOT NULL;
        ALTER TABLE "validate_correctness_ct_user" ADD "correct_answer" BOOL NOT NULL  DEFAULT True;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "task" ALTER COLUMN "client_id" SET NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "label" SET NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "final_transcription" SET NOT NULL;
        ALTER TABLE "task" ALTER COLUMN "create_date" SET NOT NULL;
        ALTER TABLE "validate_correctness_ct_user" DROP COLUMN "correct_answer";"""
