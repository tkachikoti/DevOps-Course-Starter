"""
The mongo_manager module provides a high-level interface for interacting
with a MongoDB database using PyMongo. It encapsulates database
operations into an easy-to-use class, MongoManager, which supports
common CRUD (Create, Read, Update, Delete) operations. This module
simplifies the process of connecting to MongoDB, creating collections,
and performing document manipulations such as adding, retrieving,
updating, and deleting documents.

Classes:
    MongoManager: A class to manage MongoDB operations.

"""


from pymongo import MongoClient
import mongomock
import os


class MongoDBManager:
    """
    A MongoDB management class that provides methods to interact with MongoDB.

    It supports basic CRUD operations and can be used to manage
    collections and documents in a specified MongoDB database.
    """

    def __init__(self):
        """Initializes the MongoDB client and selects the database."""
        # Check if using mock MongoDB
        if os.getenv('USE_MOCK_MONGO') == 'True':
            self.client = mongomock.MongoClient(
                f"mongodb://{os.getenv('MONGO_USER_NAME')}"
            )
        else:
            self.client = MongoClient(
                f"mongodb+srv://{os.getenv('MONGO_USER_NAME')}:"
                f"{os.getenv('MONGO_PASSWORD')}@"
                f"{os.getenv('MONGO_HOST')}/"
                f"{os.getenv('MONGO_DEFAULT_DATABASE')}?w=majority"
            )
        self.db = self.client[os.getenv("MONGO_DEFAULT_DATABASE")]

    def get_collection(self, collection_name):
        """
        Retrieves a collection from the database.

        Args:
            collection_name (str): The name of the collection to retrieve.

        Returns:
            Collection: The MongoDB collection object.
        """
        return self.db[collection_name]

    def insert_document(self, collection_name, document):
        """
        Inserts a document into a specified collection.

        Args:
            collection_name (str): The name of the collection.
            document (dict): The document to insert.

        Returns:
            ObjectId: The ID of the inserted document.
        """
        collection = self.get_collection(collection_name)
        return collection.insert_one(document).inserted_id

    def find_document(self, collection_name, query):
        """
        Finds a single document in a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query criteria to find the document.

        Returns:
            dict: The first document matching the query.
        """
        collection = self.get_collection(collection_name)
        return collection.find_one(query)

    def update_document(self, collection_name, query, new_values):
        """
        Updates a single document in a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query criteria to find the document.
            new_values (dict): The new values to update the document with.

        Returns:
            UpdateResult: The result of the update operation.
        """
        collection = self.get_collection(collection_name)
        return collection.update_one(query, {"$set": new_values})

    def delete_document(self, collection_name, query):
        """
        Deletes a single document from a collection based on a query.

        Args:
            collection_name (str): The name of the collection.
            query (dict): The query criteria to find the document.

        Returns:
            DeleteResult: The result of the delete operation.
        """
        collection = self.get_collection(collection_name)
        return collection.delete_one(query)

    def list_documents(self, collection_name):
        """
        Lists all documents in a specified collection.

        Args:
            collection_name (str): The name of the collection.

        Returns:
            list: A list of all documents in the collection.
        """
        collection = self.get_collection(collection_name)
        return list(collection.find())
