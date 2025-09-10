from pydantic_settings import BaseSettings, SettingsConfigDict

class MainSettings(BaseSettings):
    host: str
    user: str  # Change to your postgres username
    password: str # Change to your postgres password
    dbname: str
    bill_storage_path: str
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8', case_sensitive=True, extra='ignore')
