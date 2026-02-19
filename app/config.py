from pydantic_settings import BaseSettings
from pydantic import ConfigDict



class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_name: str
    database_username: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int
    
    
    # Redis config
    redis_host: str
    redis_port: str
    redis_url: str
    
    # Mailtrap settings
    mailtrap_smtp_host: str
    mailtrap_smtp_port: str
    mailtrap_smtp_user: str
    mailtrap_smtp_password: str
    mailtrap_from_email: str
    mailtrap_from_name: str
    
    
    # The SMTP settings (for production)
    smtp_host: str
    smtp_port: str
    smtp_user: str
    smtp_password: str
    

    model_config = ConfigDict(env_file=".env")

settings = Settings()