# Global config


from pydantic_settings import BaseSettings
from pydantic import Field, SecretStr

# Environment variables
class AppSettings(BaseSettings):
    PORT: int = Field(
        default=8000,
        title="Port",
        description="Port used for running the app",
        type="integer",
    )

    APP_DOMAIN: str = Field(
        default="http://localhost:8000",
        title="App domain",
        description="App domain",
        type="string",
    )

    CLIENT_DOMAIN: str = Field(
        default="http://localhost:3000",
        title="Client Domain",
        description="Client domain (e.g. http://localhost:3000)",
        type="string",
    )

    APP_NAME: str = Field(
        default="App name",
        title="App name",
        description="App name",
        type="string",
    )

    SECRET_KEY: SecretStr = Field(
        title="Secret key",
        description="Secret key used for JWT token",
    )

    ALGORITHM: str = Field(
        default="HS256",
        title="Algorithm",
        description="Algorithm used for JWT token",
        type="string",
    )

    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(
        default=33,
        title="Access token expire minutes",
        description="Access token expire minutes",
        type="integer",
    )

    MONGODB_URI: str = Field(
        default="mongodb://localhost:27017",
        title="MongoDB URI",
        description="MongoDB URI",
        type="string",
    )

    MONGODB_DB_NAME: str = Field(
        default="test",
        title="MongoDB database name",
        description="MongoDB database name",
        type="string",
    )

    SMTP_SERVER: str = Field(
        default="smtp.gmail.com",
        title="SMTP server",
        description="SMTP server used for sending email (e.g. smtp.gmail.com, smtp.mail.yahoo.com)",
        type="string",
    )

    SMTP_PORT: int = Field(
        default=587,
        title="SMTP port",
        description="SMTP port used for sending email (e.g. 587, 465)",
        type="integer",
    )

    SMTP_USERNAME: str = Field(
        default="your_email_address",
        title="SMTP username",
        description="SMTP username used for sending email",
        type="string",
    )

    SMTP_PASSWORD: SecretStr = Field(
        default="your_password",
        title="SMTP password",
        description="SMTP password used for sending email",
    )

    ADMIN_USERNAME: str = Field(
        default="admin",
        title="Admin username",
        description="Admin username",
        type="string",
    )

    ADMIN_EMAIL: str = Field(
        default="admin@gmail.com",
        title="Admin email",
        description="Admin email",
        type="string",
    )

    ADMIN_MOBILE: str = Field(
        default="01000000000",
        title="Admin mobile",
        description="Admin mobile",
        type="string",
    )

    ADMIN_PASSWORD: SecretStr = Field(
        default="admin",
        title="Admin password",
        description="Admin password which must be at least 8 characters long",
        min_length=8,
    )

    


    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


APP_SETTINGS = AppSettings()
