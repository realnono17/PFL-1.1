# app/core/config.py

import os
from dotenv import load_dotenv

load_dotenv()


class Settings:
    JWT_SECRET: str = os.getenv("JWT_SECRET", "topsecretkey")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    DATABASE_URL: str = os.getenv("DATABASE_URL")


settings = Settings()
