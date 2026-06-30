import csv
from datetime import datetime

from src.dto import Document


def parse_csv() -> list[Document]:
    documents = []
    with open("data/posts.csv", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            text = row["text"]
            created_date = datetime.strptime(row["created_date"], "%Y-%m-%d %H:%M:%S")
            rubrics = row["rubrics"][2:-2].split(sep="', '")
            documents.append(
                Document(text=text, created_date=created_date, rubrics=rubrics)
            )
    return documents
