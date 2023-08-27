# Module for Weaviate

import os

if os.getenv("OPENAI_API_KEY") is not None:
    print ("OPENAI_API_KEY is ready")
else:
    print ("OPENAI_API_KEY environment variable not found")

import weaviate
from datasets import load_dataset
import os

# Connect to your Weaviate instance
client = weaviate.Client(
    url="http://localhost:8080/",
    additional_headers={ "X-OpenAI-Api-Key": os.getenv("OPENAI_API_KEY") }
)

# Check if your instance is live and ready
# This should return `True`
client.is_ready()

# Clear up the schema, so that we can recreate it
client.schema.delete_all()
client.schema.get()

# Define the Schema object to use `text-embedding-ada-002` on `title` and `content`, but skip it for `url`
article_schema = {
    "class": "Article",
    "description": "A collection of articles",
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
          "model": "ada",
          "modelVersion": "002",
          "type": "text"
        }, 
        "qna-openai": {
          "model": "text-davinci-002",
          "maxTokens": 1600,
          "temperature": 0.0,
          "topP": 1,
          "frequencyPenalty": 0.0,
          "presencePenalty": 0.0
        }
    },
    "properties": [{
        "name": "title",
        "description": "Title of the article",
        "dataType": ["string"]
    },
    {
        "name": "content",
        "description": "Contents of the article",
        "dataType": ["text"]
    },
    {
        "name": "url",
        "description": "URL to the article",
        "dataType": ["string"],
        "moduleConfig": { "text2vec-openai": { "skip": True } }
    }]
}

# add the Article schema
client.schema.create_class(article_schema)

# get the schema to make sure it worked
client.schema.get()

### STEP 1 - load the dataset

from datasets import load_dataset
from typing import List, Iterator

# We'll use the datasets library to pull the Simple Wikipedia dataset for embedding
dataset = list(load_dataset("wikipedia", "20220301.simple")["train"])

# For testing, limited to 2.5k articles for demo purposes
# dataset = dataset[:2_500]

# Limited to 25k articles for larger demo purposes
# dataset = dataset[:25_000]

# for free OpenAI acounts, you can use 50 objects
dataset = dataset[:50]

### Step 2 - configure Weaviate Batch, with
# - starting batch size of 100
# - dynamically increase/decrease based on performance
# - add timeout retries if something goes wrong

client.batch.configure(
    batch_size=10, 
    dynamic=True,
    timeout_retries=3,
#   callback=None,
)

### Step 3 - import data

print("Importing Articles")

counter=0

with client.batch as batch:
    for article in dataset:
        if (counter %10 == 0):
            print(f"Import {counter} / {len(dataset)} ")

        properties = {
            "title": article["title"],
            "content": article["text"],
            "url": article["url"]
        }
        
        batch.add_data_object(properties, "Article")
        counter = counter+1

print("Importing Articles complete")

# Test that all data has loaded – get object count
result = (
    client.query.aggregate("Article")
    .with_fields("meta { count }")
    .do()
)
print("Object count: ", result["data"]["Aggregate"]["Article"], "\n")

# Test one article has worked by checking one object
test_article = (
    client.query
    .get("Article", ["title", "url", "content"])
    .with_limit(1)
    .do()
)["data"]["Get"]["Article"][0]

print(test_article['title'])
print(test_article['url'])
print(test_article['content'])

def qna(query, collection_name):
    
    properties = [
        "title", "content", "url",
        "_additional { answer { hasAnswer property result startPosition endPosition } distance }"
    ]

    ask = {
        "question": query,
        "properties": ["content"]
    }

    result = (
        client.query
        .get(collection_name, properties)
        .with_ask(ask)
        .with_limit(1)
        .do()
    )
    
    # Check for errors
    if ("errors" in result):
        print ("\033[91mYou probably have run out of OpenAI API calls for the current minute – the limit is set at 60 per minute.")
        raise Exception(result["errors"][0]['message'])
    
    return result["data"]["Get"][collection_name]


query_result = qna("Tell me something about Beijing", "Article")
print(query_result[0]['_additional']['answer']['result'])
# for i, article in enumerate(query_result):
#     print(f"{i+1}. { article['_additional']['answer']['result']} (Distance: {round(article['_additional']['distance'],3) })")
        
# for i, article in enumerate(query_result):
#     if article['_additional']['answer']['hasAnswer'] == False:
#       print('No answer found')
#     else:
#       print(f"{i+1}. { article['_additional']['answer']['result']} (Distance: {round(article['_additional']['distance'],3) })")

