from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "user" ADD "validate_correctness_tasks_no" INT NOT NULL  DEFAULT 0;
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "golden" SET DEFAULT True;
        CREATE TABLE IF NOT EXISTS "validate_correctness_t_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(17) NOT NULL,
    "create_date" DATE NOT NULL,
    "task_id" INT NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_validate_co_task_id_4f952b" UNIQUE ("task_id", "user_id")
);
COMMENT ON COLUMN "user"."validate_correctness_tasks_no" IS 'Number of tasks that user solve invalidate correctness task type';
COMMENT ON COLUMN "validate_correctness_t_user"."label" IS 'Correct: correct\nInCorrect: in_correct\nNotRelatedToQuran: not_related_quran\nNotMatchAya: not_match_aya\nMultipleAya: multiple_aya';;
"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "validate_correctness_t_user";
        ALTER TABLE "user" DROP COLUMN "validate_correctness_tasks_no";
        ALTER TABLE "validate_correctness_ct" ALTER COLUMN "golden" SET DEFAULT False;"""
