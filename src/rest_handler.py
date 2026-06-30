from typing import Annotated

from fastapi import Depends, Request, Response
from loguru import logger

from src.db_client import DBClient
from src.dto import DBDocument
from src.lifespan import create_app

app = create_app()


def get_db_client(request: Request) -> DBClient:
    return request.app.state.db_client


DBClientDep = Annotated[DBClient, Depends(get_db_client)]


@app.get("/documents", response_model=None)
async def get_documents_by_text(
    text: str, db_client: DBClientDep
) -> list[DBDocument] | Response:
    try:
        ids = await db_client.elastic_search_client.search(text)
        documents = await db_client.get_documents(ids)
        return [
            DBDocument(
                id=document.id,
                text=document.text,
                created_date=document.created_date,
                rubrics=document.rubrics,
            )
            for document in documents
        ]

    except Exception as e:
        logger.error(str(e))
        return Response(status_code=500)


@app.delete("/documents/{id}")
async def delete_document(id: int, db_client: DBClientDep):
    try:
        await db_client.delete_document(id)
        return Response(status_code=204)

    except Exception as e:
        logger.error(str(e))
        return Response(status_code=500)
