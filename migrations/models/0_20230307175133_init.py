from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "task" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "surra_number" INT NOT NULL,
    "aya_number" INT NOT NULL,
    "audio_file_name" VARCHAR(128) NOT NULL UNIQUE,
    "duration_ms" INT NOT NULL,
    "create_date" TIMESTAMPTZ,
    "client_id" VARCHAR(128),
    "final_transcription" TEXT,
    "label" VARCHAR(17),
    "validated" BOOL NOT NULL  DEFAULT False
);
COMMENT ON COLUMN "task"."duration_ms" IS 'length of the audio file in ms';
COMMENT ON COLUMN "task"."client_id" IS 'The id of the recitier';
COMMENT ON COLUMN "task"."label" IS 'Correct: correct\nInCorrect: in_correct\nNotRelatedToQuran: not_related_quran\nNotMatchAya: not_match_aya\nMultipleAya: multiple_aya';
CREATE TABLE IF NOT EXISTS "user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "email" VARCHAR(128) NOT NULL UNIQUE,
    "hashed_password" VARCHAR(128) NOT NULL,
    "user_role" VARCHAR(12) NOT NULL  DEFAULT 'annotator',
    "create_date" TIMESTAMPTZ NOT NULL,
    "validate_correctness_exam_pass" BOOL NOT NULL  DEFAULT False,
    "validate_correctness_tasks_no" INT NOT NULL  DEFAULT 0
);
COMMENT ON COLUMN "user"."user_role" IS 'Admin: admin\nRecitingApp: reciting_app\nAnnotator: annotator';
COMMENT ON COLUMN "user"."validate_correctness_tasks_no" IS 'Number of tasks that user solve invalidate correctness task type';
CREATE TABLE IF NOT EXISTS "validate_correctness_ct" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "surra_number" INT NOT NULL,
    "aya_number" INT NOT NULL,
    "client_id" VARCHAR(128),
    "audio_file_name" VARCHAR(128) NOT NULL UNIQUE,
    "duration_ms" INT NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL,
    "golden" BOOL NOT NULL  DEFAULT True,
    "label" VARCHAR(17) NOT NULL
);
COMMENT ON COLUMN "validate_correctness_ct"."client_id" IS 'The id of the recitier';
COMMENT ON COLUMN "validate_correctness_ct"."duration_ms" IS 'length of the audio file in ms';
COMMENT ON COLUMN "validate_correctness_ct"."label" IS 'Correct: correct\nInCorrect: in_correct\nNotRelatedToQuran: not_related_quran\nNotMatchAya: not_match_aya\nMultipleAya: multiple_aya';
CREATE TABLE IF NOT EXISTS "validate_correctness_ct_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "test" BOOL NOT NULL  DEFAULT False,
    "label" VARCHAR(17) NOT NULL,
    "correct_answer" BOOL NOT NULL  DEFAULT True,
    "create_date" TIMESTAMPTZ NOT NULL,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    "validatecorrectnessct_id" INT NOT NULL REFERENCES "validate_correctness_ct" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_validate_co_validat_6a28a8" UNIQUE ("validatecorrectnessct_id", "user_id")
);
COMMENT ON COLUMN "validate_correctness_ct_user"."test" IS 'Indicate if the answer is given for an entrance test or for  quality control';
COMMENT ON COLUMN "validate_correctness_ct_user"."label" IS 'Correct: correct\nInCorrect: in_correct\nNotRelatedToQuran: not_related_quran\nNotMatchAya: not_match_aya\nMultipleAya: multiple_aya';
CREATE TABLE IF NOT EXISTS "validate_correctness_t_user" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "label" VARCHAR(17) NOT NULL,
    "create_date" TIMESTAMPTZ NOT NULL,
    "task_id" INT NOT NULL REFERENCES "task" ("id") ON DELETE CASCADE,
    "user_id" INT NOT NULL REFERENCES "user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_validate_co_task_id_4f952b" UNIQUE ("task_id", "user_id")
);
COMMENT ON COLUMN "validate_correctness_t_user"."label" IS 'Correct: correct\nInCorrect: in_correct\nNotRelatedToQuran: not_related_quran\nNotMatchAya: not_match_aya\nMultipleAya: multiple_aya';
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
