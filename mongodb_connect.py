#this file is used to create a custom class that connects to mongodb

from pymongo import MongoClient

# connectionString = "mongodb://localhost:27017/"

# client = MongoClient(connectionString)

# db = client["teaching_assistant_db"]

# collection = db["chunks_collection"]

class DBconnect:
    def __init__ (self , connectionString , dbName , collectionName):
        self.connectionString = connectionString
        self.dbName = dbName
        self.collectionName = collectionName

        client = MongoClient(self.connectionString)
        db = client[self.dbName]
        self.collectionName = db[self.collectionName]

    
    def insert_document(self,doc):
        insert = self.collectionName.insert_one(doc)

    def find_documents(self):
        for doc in self.collectionName.find():
            print(doc)

    def find_one_document(self,find_dict):

        read = self.collectionName.find_one(find_dict)
        print(read)

    def delete_document(self,delete_dict):

        result = self.collectionName.delete_many(delete_dict)
        print("Documents deleted matching:",delete_dict)
        print("Number of documents deleted:", result.deleted_count)
dict = {
    "name":"inserted via a class" 
}

a = DBconnect("mongodb://localhost:27017/","teaching_assistant_db","chunks_collection")