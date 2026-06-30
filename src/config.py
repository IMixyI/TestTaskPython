from pydantic_settings import BaseSettings


class BackendConfig(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8067
    RELOAD: bool = True


class PostgresConfig(BaseSettings):
    HOST: str = "postgres"
    PORT: int = 5432
    USER: str = "postgres"
    DOCUMENTS_DATABASE: str = "documents_db"
    PASSWORD: str = "postgres"
    URL: str = f"postgresql+asyncpg://{USER}:{PASSWORD}@{HOST}:{PORT}/"


class ElasticSearchConfig(BaseSettings):
    HOST: str = "elasticsearch"
    PORT: int = 9200
    INDEX_NAME: str = "text_index"
    URL: str = f"http://{HOST}:{PORT}"


backend_config = BackendConfig()
postgres_config = PostgresConfig()
elastic_search_config = ElasticSearchConfig()
