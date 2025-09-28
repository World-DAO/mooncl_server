from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()


class Settings(BaseSettings):
    # MySQL数据库配置
    MYSQL_HOST: str = os.getenv("MYSQL_HOST", "43.156.89.66")
    MYSQL_PORT: int = int(os.getenv("MYSQL_PORT", "3306"))
    MYSQL_USER: str = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD: str = os.getenv("MYSQL_PASSWORD", "tpc20020602")
    MYSQL_DATABASE: str = os.getenv("MYSQL_DATABASE", "mooncl_db")

    # 构建数据库URL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    # JWT配置
    SECRET_KEY: str = os.getenv("SECRET_KEY", "")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # Celo EVM 配置
    EVM_RPC_URL: str = os.getenv("EVM_RPC_URL", "")
    NFT_CONTRACT_ADDRESS: str = os.getenv("NFT_CONTRACT_ADDRESS", "")
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
