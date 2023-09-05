MANGA = {
    "class": "Manga",
    "description": "A collection of manga panels",
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
        "name": "chapter",
        "description": "Chapter of the manga.",
        "dataType": ["string"],
        "moduleConfig": { "text2vec-openai": { "skip": True } }
    },
    {
        "name": "page",
        "description": "Page of the chapter.",
        "dataType": ["text"],
        "moduleConfig": { "text2vec-openai": { "skip": True } }
    },
    {
        "name": "content",
        "description": "Contents of the page.",
        "dataType": ["text"]
    }]
}