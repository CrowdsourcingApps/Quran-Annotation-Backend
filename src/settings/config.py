from pydantic import BaseSettings


class Settings(BaseSettings):
    MINIO_SERVER: str
    MINIO_ACCESS_KEY: str
    MINIO_SECRET_KEY: str
    MINIO_BUCKET_NAME: str
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    AUTH_SECRET_KEY: str
    Website_Email: str
    Email_Password: str
    PRIORITY_MAPPING: str
    REAL_TASKS_NO: int

    class Config:
        env_file = '.env'

    def get_minio_Bucket_url(self):
        return self.MINIO_SERVER+'/'+self.MINIO_BUCKET_NAME+'/'
