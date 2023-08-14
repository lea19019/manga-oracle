import easyocr
reader = easyocr.Reader(['en',]) # this needs to run only once to load the model into memory
result = reader.readtext('./jjk-manga/231/jjk_231_002.png')
for r in result:
    print(r)