from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, async_sessionmaker

from src.dto import TextMapping
from src.elastic_search_client import ElasticSearchClient
from src.sql_models import DocumentModel


class DBClient:
    def __init__(self, engine: AsyncEngine, elastic_search_client: ElasticSearchClient):
        self.engine = engine
        self.elastic_search_client = elastic_search_client
        self.async_session_maker = async_sessionmaker(
            bind=engine, class_=AsyncSession, expire_on_commit=False
        )

    async def stop(self) -> None:
        await self.engine.dispose()
        await self.elastic_search_client.close()

    async def add_documents(self, documents: list[DocumentModel]) -> None:
        try:
            async with self.async_session_maker() as session:
                for document in documents:
                    session.add(document)

                await session.flush()

                text_mapping = [
                    TextMapping(id=doc.id, text=doc.text) for doc in documents
                ]
                await self.elastic_search_client.index_documents_bulk(text_mapping)
                await session.commit()

        except Exception:
            await session.rollback()
            raise

    async def delete_document(self, document_id: int) -> None:
        try:
            async with self.async_session_maker() as session:
                await session.execute(
                    delete(DocumentModel).where(DocumentModel.id == document_id)
                )
                await self.elastic_search_client.delete_document(document_id)
                await session.commit()

        except Exception:
            await session.rollback()
            raise

    async def get_documents(self, documents_ids: list[int]) -> list[DocumentModel]:
        try:
            async with self.async_session_maker() as session:
                result = await session.execute(
                    select(DocumentModel)
                    .where(DocumentModel.id.in_(documents_ids))
                    .order_by(DocumentModel.created_date)
                    .limit(20)
                )
                return list(result.scalars().all())

        except Exception:
            await session.rollback()
            raise
