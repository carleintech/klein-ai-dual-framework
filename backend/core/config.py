from pydantic import BaseModel
from typing import List
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseModel):
    # Elastic Configuration
    elastic_cloud_id: str = os.getenv("ELASTIC_CLOUD_ID", "")
    elastic_user: str = os.getenv("ELASTIC_USER", "")
    elastic_pass: str = os.getenv("ELASTIC_PASS", "")
    elastic_endpoint: str = os.getenv("ELASTIC_ENDPOINT", "")
    elastic_api_key: str = os.getenv("ELASTIC_API_KEY", "")

    # Google Cloud Configuration
    gcp_project: str = os.getenv("GCP_PROJECT", "")
    gcp_location: str = os.getenv("GCP_LOCATION", "us-central1")
    vertex_model: str = os.getenv("VERTEX_MODEL", "text-bison@001")

    # Service Flags
    energy_mode: str = os.getenv("ENERGY_MODE", "normal")
    allow_shutdown: bool = os.getenv("ALLOW_SHUTDOWN", "true").lower() == "true"

    # CORS Configuration
    cors_origins: List[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")

    # Application Settings
    app_name: str = "Klein AI Dual Framework"
    app_version: str = "1.0.0"

settings = Settings()
