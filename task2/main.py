import scrap
import json
from pymongo import MongoClient
from pymongo.server_api import ServerApi

def some_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            return "No more page."
        except IndexError:
            return "IE"
        except UnboundLocalError:
            return "ULE"
        except AttributeError:
            return "AE"
    return inner

def create_files(data):
    try:
        if data:
            print("Create files...")
            for name in list(data.keys()):
                file_name = name + '.json'
                with open(file_name, 'w', encoding='utf-8') as f:
                    json.dump(data.get(name), f, ensure_ascii=False, indent=4)
            return list(data.keys())
        else:
            print("No data to record")
            return []
    except Exception as e:
        print(f"Error in create files: {e}")

def get_files(list):
    try:
        file_list = []
        for item in list:
            file_name = item + '.json'
            file_list.append(file_name)
        return file_list
    except Exception as e:
        print(f"Errow in create file list: {e}")
        return []

def import_json_to_mongodb(collection_list, file_list):
    try:
        if collection_list:
            print("Export data to Mongo.")
            for collection_name, file in zip(collection_list, file_list):
                print(f"Export data to collection {collection_name}")
                with open(file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    collection = db[collection_name]
                    if isinstance(data, list):
                        collection.insert_many(data)
                    else:
                        collection.insert_one(data) 
            print("Sucess export.")
        else:
            print("No data to export.")
    except Exception as e:
        print(f"Error in export data to Mongo: {e}")
    
if __name__ == "__main__":
    url = 'https://quotes.toscrape.com'
    data = scrap.main(url)
    
    
    client = MongoClient(
        "mongodb+srv://YShkolnyi:Stokrotka_13@cluster0.7wu4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
        server_api=ServerApi('1')
    )
    db = client.GOIT_ds_hw03
    
    collection_list = create_files(data)
    files_list = get_files(collection_list)
    import_json_to_mongodb(collection_list,files_list)
    print("END ;)")