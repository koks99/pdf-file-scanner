from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import gridfs

uri = "mongodb+srv://kokulan99:koku1999@mongocluster.tb95q.mongodb.net/?retryWrites=true&w=majority&appName=MongoCluster"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
mydb = client["mydatabase"]
pdf_col = mydb["pdf"]

image_db = client["pdf_images_db"]
fs = gridfs.GridFS(image_db)