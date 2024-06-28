from pymongo import MongoClient

def connect_to_mongodb(connection_string):
    """ Connect to MongoDB and return the MongoClient object """
    try:
        client = MongoClient(connection_string)
        print("Connected successfully to MongoDB!")
        return client
    except Exception as e:
        print(f"Error connecting to MongoDB: {e}")
        return None

def retrieve_data(client, db_name, collection_name):
    """ Retrieve data from MongoDB collection and return as a list of documents """
    try:
        db = client[db_name]
        collection = db[collection_name]
        cursor = collection.find({})
        documents = list(cursor)
        print(f"Retrieved {len(documents)} documents from collection '{collection_name}'")
        return documents
    except Exception as e:
        print(f"Error retrieving data from MongoDB: {e}")
        return []

def clean_document(document):
    """ Clean individual document fields dynamically """
    try:
        # Iterate through each field in the document
        cleaned_document = {}
        for key, value in document.items():
            # Example: Clean numeric fields
            if isinstance(value, (int, float)):
                cleaned_document[key] = value
            # Example: Clean string fields
            elif isinstance(value, str):
                cleaned_document[key] = value.strip()  # Strip whitespace

            # Add more cleaning rules based on field inspection...

        # Print message after cleaning each document
        print(f"Document cleaned and processed: {document['_id']}")

        return cleaned_document
    except Exception as e:
        print(f"Error cleaning document: {e}")
        return None

def save_to_mongodb(cleaned_documents, client, db_name, new_collection_name):
    """ Save cleaned documents to a new collection in MongoDB """
    try:
        db = client[db_name]
        collection = db[new_collection_name]
        collection.insert_many(cleaned_documents)
        print(f"Cleaned data saved successfully to MongoDB collection '{new_collection_name}'")
    except Exception as e:
        print(f"Error saving cleaned data to MongoDB: {e}")

def main():
    # Replace with your MongoDB connection string and collection details
    connection_string = "mongodb+srv://bharathwajravi:FxcugqUZncJSZU4u@cluster0.yid1esl.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    db_name = 'Airbub_Analysis'
    original_collection_name = 'AIRBUB'
    new_collection_name = 'CLEANED_AIRBUB'

    # Connect to MongoDB
    client = connect_to_mongodb(connection_string)

    if client:
        # Retrieve documents from MongoDB
        documents = retrieve_data(client, db_name, original_collection_name)

        if documents:
            # Clean each document dynamically
            cleaned_documents = []
            for doc in documents:
                cleaned_doc = clean_document(doc)
                if cleaned_doc:
                    cleaned_documents.append(cleaned_doc)

            # Save cleaned documents to a new collection
            save_to_mongodb(cleaned_documents, client, db_name, new_collection_name)

        # Close the MongoDB connection
        client.close()
        print("MongoDB connection closed.")

if __name__ == "__main__":
    main()
