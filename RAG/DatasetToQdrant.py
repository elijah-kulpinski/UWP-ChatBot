# Import the OpenAI library for accessing OpenAI's API services
import openai
# Import the QdrantClient and PointStruct from the qdrant_client package for interacting with the Qdrant API
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct

# Initialize the OpenAI client with your API key
openai_client = openai.Client(api_key="OPEN_AI_API_KEY")
# Initialize the Qdrant client with the cluster URL and API key
qdrant_client = QdrantClient(url="QDRANT_CLUSTER_URL", api_key="QDRANT_API_KEY")
# Define the embedding model to be used for generating text embeddings
embedding_model = "text-embedding-3-small"
# Specify the name of the collection in Qdrant where the data will be stored
collection_name = "ChatbotDataset"

# Calculate the total number of lines in the dataset file
total_lines = sum(1 for line in open('Dataset.txt'))
# Define the size of each chunk to process (number of lines at a time)
chunk_size = 100
# Initialize the starting index
start = 0

# Loop through the dataset file in chunks
while start < total_lines:
    with open('Dataset.txt', 'r') as file:
        lines = file.readlines()[start:start+chunk_size]  # Read a chunk of lines from the file
    
    # Strip whitespace from each line and create a list of texts
    texts = [line.strip() for line in lines]
    points = []  # Initialize a list to store points to be inserted into Qdrant

    # Process each text to create points for Qdrant
    for idx, text in enumerate(texts):
        try:
            # Generate an embedding for the text using OpenAI's model
            result = openai_client.embeddings.create(input=text, model=embedding_model)
            # Create a point with the embedding, a unique ID, and the original text as payload
            point = PointStruct(
                id=idx+start,
                vector=result.data[0].embedding,
                payload={"text": text},
            )
            points.append(point)  # Add the point to the list
        except Exception as e:
            # Handle exceptions (e.g., API errors) and print an error message
            print(f"Error on line {idx}: {e}")
            continue

    # Insert or update points in the specified Qdrant collection
    qdrant_client.upsert(collection_name, points)
    # Move the start index forward by the chunk size
    start += chunk_size
