from dotenv import load_dotenv
import os

class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            load_dotenv()  # Load environment variables
        return cls._instance

    @property
    def database_url(self):
        return os.getenv("DATABASE_URL")

    @property
    def secret_key(self):
        return os.getenv("SECRET_KEY")

config = Config()
