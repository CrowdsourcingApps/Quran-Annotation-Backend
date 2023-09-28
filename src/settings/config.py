from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_HOST: str
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str
    AUTH_SECRET_KEY: str
    Website_Email: str
    Email_Password: str
    PRIORITY_MAPPING: str
    REAL_TASKS_NO: int
    Audio_URL: str
    FIREBASE_SETTINGS: str
    FRONT_END: str

    class Config:
        env_file = '.env'

    def get_audio_url(self):
        return self.Audio_URL+'/'
