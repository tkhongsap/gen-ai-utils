"""
Configuration Management - Centralized configuration with environment support

Provides type-safe configuration management using Pydantic with support for
environment variables, .env files, and configuration validation.
"""

import os
from typing import Optional, Dict, Any
from pathlib import Path
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings
from dotenv import load_dotenv


class OpenAIConfig(BaseModel):
    """OpenAI API configuration"""
    api_key: str = Field(..., description="OpenAI API key")
    organization: Optional[str] = Field(None, description="OpenAI organization ID")
    model: str = Field("gpt-4", description="Default model to use")
    temperature: float = Field(0.7, ge=0, le=2, description="Temperature for generation")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens in response")
    timeout: int = Field(60, description="Request timeout in seconds")


class LlamaParseConfig(BaseModel):
    """LlamaParse API configuration"""
    api_key: str = Field(..., description="LlamaParse API key")
    result_type: str = Field("markdown", description="Result format (markdown or text)")
    verbose: bool = Field(True, description="Enable verbose logging")


class DatabaseConfig(BaseModel):
    """Database configuration"""
    host: str = Field("localhost", description="Database host")
    port: int = Field(5432, description="Database port")
    database: str = Field("genai_utils", description="Database name")
    username: str = Field("postgres", description="Database username")
    password: str = Field(..., description="Database password")
    pool_size: int = Field(10, description="Connection pool size")

    @property
    def connection_string(self) -> str:
        """Get PostgreSQL connection string"""
        return f"postgresql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"


class RedisConfig(BaseModel):
    """Redis configuration"""
    host: str = Field("localhost", description="Redis host")
    port: int = Field(6379, description="Redis port")
    db: int = Field(0, description="Redis database number")
    password: Optional[str] = Field(None, description="Redis password")
    ttl: int = Field(3600, description="Default TTL in seconds")


class APIConfig(BaseModel):
    """API server configuration"""
    host: str = Field("0.0.0.0", description="API host")
    port: int = Field(8000, description="API port")
    debug: bool = Field(False, description="Debug mode")
    workers: int = Field(4, description="Number of workers")
    cors_origins: list = Field(["*"], description="CORS allowed origins")


class LoggingConfig(BaseModel):
    """Logging configuration"""
    level: str = Field("INFO", description="Logging level")
    format: str = Field("json", description="Log format (json or text)")
    file_path: Optional[str] = Field(None, description="Log file path")
    max_bytes: int = Field(10485760, description="Max log file size (10MB)")
    backup_count: int = Field(5, description="Number of backup files")


class Config(BaseSettings):
    """Main application configuration"""

    # Environment
    env: str = Field("development", description="Environment (development, staging, production)")
    debug: bool = Field(False, description="Debug mode")

    # OpenAI
    openai_api_key: str = Field(..., env="OPENAI_API_KEY")
    openai_organization: Optional[str] = Field(None, env="OPENAI_ORGANIZATION")
    openai_model: str = Field("gpt-4", env="OPENAI_MODEL")
    openai_temperature: float = Field(0.7, env="OPENAI_TEMPERATURE")

    # LlamaParse
    llama_cloud_api_key: Optional[str] = Field(None, env="LLAMA_CLOUD_API_KEY")

    # Database
    db_host: str = Field("localhost", env="DB_HOST")
    db_port: int = Field(5432, env="DB_PORT")
    db_name: str = Field("genai_utils", env="DB_NAME")
    db_user: str = Field("postgres", env="DB_USER")
    db_password: str = Field("", env="DB_PASSWORD")

    # Redis
    redis_host: str = Field("localhost", env="REDIS_HOST")
    redis_port: int = Field(6379, env="REDIS_PORT")
    redis_password: Optional[str] = Field(None, env="REDIS_PASSWORD")

    # API
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_workers: int = Field(4, env="API_WORKERS")

    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "allow"

    @property
    def openai(self) -> OpenAIConfig:
        """Get OpenAI configuration"""
        return OpenAIConfig(
            api_key=self.openai_api_key,
            organization=self.openai_organization,
            model=self.openai_model,
            temperature=self.openai_temperature
        )

    @property
    def llama_parse(self) -> Optional[LlamaParseConfig]:
        """Get LlamaParse configuration"""
        if not self.llama_cloud_api_key:
            return None
        return LlamaParseConfig(api_key=self.llama_cloud_api_key)

    @property
    def database(self) -> DatabaseConfig:
        """Get database configuration"""
        return DatabaseConfig(
            host=self.db_host,
            port=self.db_port,
            database=self.db_name,
            username=self.db_user,
            password=self.db_password
        )

    @property
    def redis(self) -> RedisConfig:
        """Get Redis configuration"""
        return RedisConfig(
            host=self.redis_host,
            port=self.redis_port,
            password=self.redis_password
        )

    @property
    def api(self) -> APIConfig:
        """Get API configuration"""
        return APIConfig(
            host=self.api_host,
            port=self.api_port,
            workers=self.api_workers,
            debug=self.debug
        )

    @property
    def logging(self) -> LoggingConfig:
        """Get logging configuration"""
        return LoggingConfig(
            level=self.log_level,
            format=self.log_format
        )


def load_config(env_file: Optional[str] = None) -> Config:
    """
    Load configuration from environment

    Args:
        env_file: Optional path to .env file

    Returns:
        Config instance
    """
    if env_file:
        load_dotenv(env_file)
    else:
        # Try to load from common locations
        for env_path in [".env", "../.env", "../../.env"]:
            if Path(env_path).exists():
                load_dotenv(env_path)
                break

    return Config()


# Global config instance
_config: Optional[Config] = None


def get_config() -> Config:
    """
    Get global config instance (singleton)

    Returns:
        Config instance
    """
    global _config
    if _config is None:
        _config = load_config()
    return _config


def reload_config(env_file: Optional[str] = None):
    """
    Reload configuration from environment

    Args:
        env_file: Optional path to .env file
    """
    global _config
    _config = load_config(env_file)
