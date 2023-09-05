import easyocr
import os
from .wv import load_data

reader = easyocr.Reader(['en',]) # this needs to run only once to load the model into memory

def get_data(path):
    data = []
    for filename in os.listdir(path):
        if not filename.endswith(".png"): continue
        result = reader.readtext(path+filename, paragraph=True, detail=0)
        content = "\n".join(res for res in result).lower()
        if len(content) < 10: continue
        filename = filename[:-4].split("_")
        chapter, page = filename[1], filename[2]
        data.append({"chapter": chapter, "page": page, "content": content})
    return data

# Write a function that takes a path and checks for all subfolders and if it is a subfolder
# it will call the get_data function and return the data, then it will call the load_data function
def load_data_from_folder(path):
    for folder in os.listdir(path):
        if not os.path.isdir(path+folder): continue
        print("Loading data from", folder)
        print(path+folder+"/")
        data = get_data(path+folder+"/")
        load_data(data)
