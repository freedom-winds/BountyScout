import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # GitHub
    GITHUB_TOKEN: str = os.environ.get("GITHUB_TOKEN", "")

    # Bounty scanning
    BOUNTY_REPOSITORIES: str = os.environ.get(
        "BOUNTY_REPOSITORIES",
        "MyZubster-Ecosystem/myzubster,Nudge-Pay/nudge-server,"
        "Perenna-Labs/perenna-contracts,Sottara-Labs/sottara,"
        "klineodyssey/kline-odyssey",
    )
    SCAN_INTERVAL_SECONDS: int = int(os.environ.get("SCAN_INTERVAL_SECONDS", "3600"))

    # Output
    OUTPUT_DIR: str = os.environ.get(
        "OUTPUT_DIR",
        str(Path(__file__).parent.parent.parent / "output"),
    )

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
