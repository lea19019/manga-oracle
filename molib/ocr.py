# Module for EasyOCR
import easyocr
import os
reader = easyocr.Reader(['en',]) # this needs to run only once to load the model into memory
# Open folder ./jjk-manga/231/ and for every image in the folder, run the OCR
path = "./jjk-manga/231/"
# for filename in os.listdir(path):
#     if filename.endswith(".png"):
#         print(filename)
#         # result = reader.readtext(path+filename)
#         # print(result)
#         continue
#     else:
#         continue


result = reader.readtext('./jjk-manga/231/jjk_231_002.png', paragraph=True, detail=0)
for res in result:
    print(res)