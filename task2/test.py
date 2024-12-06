import main
from pymongo import MongoClient
from pymongo.server_api import ServerApi

client = MongoClient(
        "mongodb+srv://YShkolnyi:Stokrotka_13@cluster0.7wu4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1')
    )
db = client.GOIT_ds_hw03

data = {'test1':[{'a':1,'b':2},{'a':3,'b':4}],'test2':[{'q':5,'w':6},{'q':7,'w':8}]}


collection_list = main.create_files(data)
files_list = main.get_files(collection_list)
main.import_json_to_mongodb(collection_list,files_list)
print("Імпорт завершено.")

# @some_error
# def create_files(data):
#     if data:
#         for name in list(data.keys()):
#             file_name = name + '.json'
#             with open(file_name, 'w', encoding='utf-8') as f:
#                 json.dump(data.get(name), f, ensure_ascii=False, indent=4)
#         return list(data.keys())

# @some_error
# def get_files(list):
#     file_list = []
#     for item in list:
#         file_name = item + '.json'
#         file_list.append(file_name)
#     return file_list

# @some_error
# def import_json_to_mongodb(collection_list, file_list):
#     if collection_list:
#         for collection, file in zip(collection_list,file_list):
#             with open(file, 'r', encoding='utf-8') as file:
#                 data = json.load(file)
#                 if isinstance(data, list):
#                     collection.insert_many(data)
#                 else:
#                     collection.insert_one(data)