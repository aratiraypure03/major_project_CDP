import pandas as pd
from pymongo import MongoClient
from urllib.parse import quote_plus

# MongoDB Connection Details
username = "mohitdb"  # Replace with your MongoDB username
password = "mohitdb"  # Replace with your MongoDB password
encoded_username = quote_plus(username)
encoded_password = quote_plus(password)

# MongoDB URI
MONGO_URI = f"mongodb+srv://{encoded_username}:{encoded_password}@cluster.hfyt1.mongodb.net/plant_disease_db?retryWrites=true&w=majority"

# Initialize MongoDB client
try:
    client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
    db = client['plant_disease_db']  # Database name
    print("MongoDB connection successful.")
except Exception as e:
    print(f"Error connecting to MongoDB: {e}")
    exit()

# Function to upload CSV to MongoDB
def upload_csv_to_mongo(csv_path, collection_name):
    try:
        # Read CSV into a DataFrame
        df = pd.read_csv(csv_path, encoding='ISO-8859-1')

        # Convert DataFrame to a list of dictionaries (JSON format)
        data = df.to_dict(orient="records")

        # Insert data into MongoDB collection
        db[collection_name].insert_many(data)
        print(f"✅ Successfully uploaded {len(data)} records to '{collection_name}' collection.")
    except Exception as e:
        print(f"❌ Error uploading {csv_path} to MongoDB: {e}")

# Upload CSV files
upload_csv_to_mongo("disease_info.csv", "disease_info")
upload_csv_to_mongo("supplement_info1.csv", "supplements")

# Close MongoDB connection
client.close()
print("MongoDB connection closed.")