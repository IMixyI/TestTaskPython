from elasticsearch import AsyncElasticsearch, helpers

from src.dto import TextMapping


class ElasticSearchClient:
    def __init__(self, elastic_search_client: AsyncElasticsearch, index_name: str):
        self.client = elastic_search_client
        self.index_name = index_name

    async def index_documents_bulk(self, text_mappings: list[TextMapping]):
        actions = [
            {
                "_index": self.index_name,
                "_id": str(text_mapping.id),
                "_source": {"text": text_mapping.text},
            }
            for text_mapping in text_mappings
        ]
        await helpers.async_bulk(self.client, actions)

    async def search(self, text: str) -> list[int] | None:
        search_query = {"query": {"match": {"text": text}}}

        response = await self.client.search(index=self.index_name, body=search_query)

        return [int(hit["_id"]) for hit in response["hits"]["hits"]]

    async def delete_document(self, document_id) -> None:
        await self.client.delete(index=self.index_name, id=str(document_id))

    async def close(self):
        await self.client.close()
