from pymongo import MongoClient
from pymongo.server_api import ServerApi
from faker import Faker

fake = Faker('uk_UA')

client = MongoClient(
    "mongodb+srv://YShkolnyi:Stokrotka_13@cluster0.7wu4k.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0",
    server_api=ServerApi('1')
)

db = client.GOIT_ds_hw03

for _ in range(10):
    result_one = db.hamsters.insert_one(
        {
            "name": fake.unique.first_name(),
            "age": fake.random_int(min=1, max=5),
            "features": [fake.sentence(nb_words=2).rstrip('.') for _ in range(3)],
        }
    )
    print(result_one.inserted_id)


