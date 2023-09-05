import weaviate
import os
from .schema import MANGA

if not os.getenv("OPENAI_API_KEY"): raise Exception("OPENAI_API_KEY environment variable not found")
client = weaviate.Client(
    url="http://localhost:8080/",
    additional_headers={ "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY") }
)
if not client.is_ready(): raise Exception("Weaviate is not ready")

# Prepare the schema
def prepare_schema():
    client.schema.delete_all()
    client.schema.create_class(MANGA)
    client.batch.configure(
        batch_size=25, 
        dynamic=True,
        timeout_retries=3
    )

prepare_schema()

def load_data(dataset):
    with client.batch as batch:
        for page in dataset:
            properties = {
                "chapter": page["chapter"],
                "page": page["page"],
                "content": page["content"]
            }
            batch.add_data_object(properties, "Manga")

    # Test that all data has loaded – get object count
    result = (client.query.aggregate("Manga").with_fields("meta { count }").do())
    print("Object count: ", result["data"]["Aggregate"]["Manga"], "\n")


def qna(query):
    properties = [
        "chapter", "page", "content"
        "_additional { answer { hasAnswer property result startPosition endPosition } distance }"
    ]

    ask = {
        "question": query,
        "properties": ["content"]
    }

    result = (
        client.query
        .get("Manga", properties)
        .with_ask(ask)
        .with_limit(6)
        .do()
    )
    
    # Check for errors
    if ("errors" in result):
        print ("\033[91mYou probably have run out of OpenAI API calls for the current minute – the limit is set at 60 per minute.")
        raise Exception(result["errors"][0]['message'])
    
    return result["data"]["Get"]["Manga"]
