from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # 应用配置
    APP_NAME: str = "MoonCL Server"
    APP_VERSION: str = "1.0.0"

    # MySQL数据库配置
    MYSQL_HOST: str = "43.156.89.66"
    MYSQL_PORT: int = 3306
    MYSQL_USER: str = "root"
    MYSQL_PASSWORD: str = "tpc20020602"
    MYSQL_DATABASE: str = "mooncl_db"

    # 构建数据库URL
    @property
    def DATABASE_URL(self) -> str:
        return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    # JWT配置
    SECRET_KEY: str = ""
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7天

    # NFT配置
    NFT_CONTRACT_ADDRESS: str = ""

    # Sui配置
    SUI_RPC_URL: str = "https://fullnode.testnet.sui.io:443"
    SUI_PACKAGE_ID: str = ""
    SUI_NETWORK: str = "testnet"

    class Config:
        env_file = ".env"


settings = Settings()
