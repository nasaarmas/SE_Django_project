from pymongo import MongoClient
from ipr_app.settings import MONGO_DB_USERNAME, MONGO_DB_PASSWORD, MONGO_DB_HOST, MONGO_DB_NAME
# connect with mongodb
client = MongoClient(host=MONGO_DB_HOST,
                     port=int(27017),
                     username=MONGO_DB_USERNAME,
                     password=MONGO_DB_PASSWORD
                     )

MongoDB = client[MONGO_DB_NAME]

