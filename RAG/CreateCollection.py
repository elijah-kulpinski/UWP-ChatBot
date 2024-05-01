# Import necessary classes from the qdrant_client package
from qdrant_client import QdrantClient, models

# Initialize the QdrantClient object with the URL and API key for the Qdrant cluster
client = QdrantClient(
    url="QDRANT_CLUSTER_URL",  # Replace "QDRANT_CLUSTER_URL" with the actual URL of your Qdrant cluster
    api_key="QDRANT_API_KEY",  # Replace "QDRANT_API_KEY" with the actual API key for authentication
)

# The following line, when uncommented, deletes a collection named 'ChatbotDataset' from the Qdrant database
# client.delete_collection(collection_name="ChatbotDataset")

# The next line, when uncommented, creates a new collection named 'ChatbotDataset'
# with a vector configuration specifying the vector size and the distance metric (COSINE in this case)
# client.create_collection(collection_name="ChatbotDataset", vectors_config=models.VectorParams(size=1536, distance=models.Distance.COSINE))

# Retrieves and prints the configuration and status of the collection named 'ChatbotDataset'
print(client.get_collection(collection_name="ChatbotDataset"))

# The last commented line, when uncommented, prints all collections available in the Qdrant cluster
# print(client.get_collections())
