from contextlib import asynccontextmanager

from elasticsearch import AsyncElasticsearch
from fastapi import FastAPI
from sqlalchemy.ext.asyncio import create_async_engine

from src.config import elastic_search_config, postgres_config
from src.csv_parse import parse_csv
from src.db_client import DBClient
from src.elastic_search_client import ElasticSearchClient
from src.sql_models import DocumentModel, create_table


@asynccontextmanager
async def lifespan(app: FastAPI):
    documents_db_engine = create_async_engine(
        postgres_config.URL + postgres_config.DOCUMENTS_DATABASE
    )
    elastic_search = AsyncElasticsearch(elastic_search_config.URL)
    await elastic_search.indices.create(
        index=elastic_search_config.INDEX_NAME, ignore=400
    )
    elastic_search_client = ElasticSearchClient(
        elastic_search, elastic_search_config.INDEX_NAME
    )

    db_client = DBClient(documents_db_engine, elastic_search_client)

    if not await create_table(documents_db_engine):
        documents = [DocumentModel(**document.model_dump()) for document in parse_csv()]
        await db_client.add_documents(documents)

    app.state.db_client = db_client

    yield

    await db_client.stop()


def create_app() -> FastAPI:
    app = FastAPI(lifespan=lifespan)
    return app
