from functools import lru_cache
from pydantic import EmailStr, Field
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Banco de dados
    DATABASE_URL: str = Field(..., description="URL completa do banco de dados")

    # JWT
    SECRET_KEY: str = Field(..., description="Chave secreta para geração de tokens")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 horas

    # Email (SMTP)
    SMTP_SERVER: str = Field(default="smtp.gmail.com", description="Servidor SMTP")
    SMTP_PORT: int = Field(default=587, description="Porta SMTP")
    SMTP_USERNAME: str = Field(default="", description="Usuário do SMTP")
    SMTP_PASSWORD: str = Field(default="", description="Senha do SMTP")

    # Twilio / WhatsApp
    TWILIO_ACCOUNT_SID: str = Field(default="", description="SID da conta Twilio")
    TWILIO_AUTH_TOKEN: str = Field(default="", description="Token de autenticação Twilio")
    TWILIO_WHATSAPP_FROM: str = Field(default="whatsapp:+14155238886", description="Número do remetente do WhatsApp Twilio")

    # Info da aplicação
    APP_NAME: str = Field(default="BMHE Analytics", description="Nome da aplicação")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()
