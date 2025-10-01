from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
from typing import List, Dict, Any

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

    # EVM 配置
    EVM_RPC_URL: str = os.getenv("EVM_RPC_URL", "")
    POLKADOT_RPC_URL: str = os.getenv("POLKADOT_RPC_URL", "")
    NFT_CONTRACT_ADDRESS: str = os.getenv("NFT_CONTRACT_ADDRESS", "")
    POLKADOT_NFT_CONTRACT_ADDRESS: str = os.getenv("POLKADOT_NFT_CONTRACT_ADDRESS", "")
    LAUNCHPAD_CONTRACT_ADDRESS: str = os.getenv("LAUNCHPAD_CONTRACT_ADDRESS", "")
    POLKADOT_LAUNCHPAD_CONTRACT_ADDRESS: str = os.getenv(
        "POLKADOT_LAUNCHPAD_CONTRACT_ADDRESS", ""
    )
    PRIVATE_KEY: str = os.getenv("PRIVATE_KEY", "")

    # AI评估配置
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # EigenLayer基础配置
    EIGEN_RPC_URL: str = os.getenv(
        "EIGEN_RPC_URL", "https://ethereum-holesky-rpc.publicnode.com"
    )
    EIGEN_AVS_CONTRACT: str = os.getenv("EIGEN_AVS_CONTRACT", "")
    EIGEN_OPERATOR_PRIVATE_KEY: str = os.getenv("EIGEN_OPERATOR_PRIVATE_KEY", "")
    EIGEN_SLASHING_CONTRACT: str = os.getenv("EIGEN_SLASHING_CONTRACT", "")

    # EigenCloud DevKit配置
    DEVKIT_ENABLED: bool = os.getenv("DEVKIT_ENABLED", "false").lower() == "true"
    DEVKIT_PROJECT_PATH: str = os.getenv("DEVKIT_PROJECT_PATH", "./avs-project")
    DEVKIT_NETWORK: str = os.getenv("DEVKIT_NETWORK", "devnet")

    # Hourglass任务框架配置
    HOURGLASS_ENABLED: bool = os.getenv("HOURGLASS_ENABLED", "true").lower() == "true"
    HOURGLASS_TASK_TIMEOUT: int = int(os.getenv("HOURGLASS_TASK_TIMEOUT", "300"))
    HOURGLASS_MAX_RETRIES: int = int(os.getenv("HOURGLASS_MAX_RETRIES", "3"))

    # AVS验证配置
    AVS_VERIFICATION_ENDPOINT: str = os.getenv(
        "AVS_VERIFICATION_ENDPOINT", "http://localhost:8080/verify"
    )
    AVS_AGGREGATOR_ENDPOINT: str = os.getenv(
        "AVS_AGGREGATOR_ENDPOINT", "http://localhost:8081/aggregate"
    )

    # AVS配置
    AVS_NAME: str = "MoonCL-AI-Evaluator"
    AVS_VERSION: str = "1.0.0"
    MIN_OPERATOR_STAKE: float = 32.0
    CONSENSUS_THRESHOLD: int = 2

    # 操作员配置
    EIGEN_OPERATORS: str = os.getenv("EIGEN_OPERATORS", "")
    EVALUATION_TIMEOUT: int = int(os.getenv("EVALUATION_TIMEOUT", "120"))
    MAX_PRICE_DEVIATION: float = float(os.getenv("MAX_PRICE_DEVIATION", "0.3"))
    SLASHING_PERCENTAGE: float = float(os.getenv("SLASHING_PERCENTAGE", "0.1"))

    # 获取操作员列表
    @property
    def OPERATORS_LIST(self) -> List[Dict[str, Any]]:
        if self.EIGEN_OPERATORS:
            try:
                import json

                return json.loads(self.EIGEN_OPERATORS)
            except:
                pass
        # 默认操作员列表
        return [
            {
                "address": "0x1234567890123456789012345678901234567890",
                "stake": 100.0,
                "reputation": 0.95,
            },
            {
                "address": "0x2345678901234567890123456789012345678901",
                "stake": 150.0,
                "reputation": 0.92,
            },
            {
                "address": "0x3456789012345678901234567890123456789012",
                "stake": 200.0,
                "reputation": 0.98,
            },
        ]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
