from pymongo import MongoClient

db_client = MongoClient(
    "mongodb+srv://zupay-pymongo:f8ptB7wAaZJtLfBC@deathcrafter.tmdy1.mongodb.net/?retryWrites=true&w=majority"
).get_database("zupay-fastapi-blog")
