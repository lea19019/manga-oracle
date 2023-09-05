from molib import ocr

ocr.load_data_from_folder("./jjk-manga/")

# path = "./jjk-manga/231/"
# chapter_231 = get_data(path)
# Test one article has worked by checking one object
# test_article = (
#     client.query
#     .get("Article", ["title", "url", "content"])
#     .with_limit(1)
#     .do()
# )["data"]["Get"]["Article"][0]

# print(test_article['title'])
# print(test_article['url'])
# print(test_article['content'])


# query_result = qna("Tell me something about Beijing")
# print(query_result[0]['_additional']['answer']['result'])
# for i, article in enumerate(query_result):
#     print(f"{i+1}. { article['_additional']['answer']['result']} (Distance: {round(article['_additional']['distance'],3) })")
        
# for i, article in enumerate(query_result):
#     if article['_additional']['answer']['hasAnswer'] == False:
#       print('No answer found')
#     else:
#       print(f"{i+1}. { article['_additional']['answer']['result']} (Distance: {round(article['_additional']['distance'],3) })")

