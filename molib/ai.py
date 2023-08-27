# Module for LLM, using OpenAI
import openai

def get_embedding(text: str, model="text-embedding-ada-002"):
   text = text.replace("\n", " ")
   return openai.Embedding.create(input = [text], model=model)['data'][0]['embedding']
