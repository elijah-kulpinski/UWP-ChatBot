// Import the OpenAI client library for accessing OpenAI APIs
import { OpenAI } from 'openai';
// Import the QdrantClient from the Qdrant JavaScript client package for REST API interactions
import { QdrantClient } from "@qdrant/js-client-rest";

// Initialize the OpenAI client with your API key
const openai_client = new OpenAI({
  apiKey: 'OPEN_AI_API_KEY',  // Replace 'OPEN_AI_API_KEY' with your actual OpenAI API key
});

// Initialize the Qdrant client with the cluster URL and API key
const qdrant_client = new QdrantClient({
  url: 'QDRANT_CLUSTER_URL',  // Replace 'QDRANT_CLUSTER_URL' with your actual Qdrant cluster URL
  apiKey: 'QDRANT_API_KEY',  // Replace 'QDRANT_API_KEY' with your actual Qdrant API key
});

// Define the text input for which to generate an embedding
const text = 'scholarships';

// Generate an embedding for the input text using OpenAI's embedding model
const openaiResponse = await openai_client.embeddings.create({
  input: text, 
  model: 'text-embedding-3-small'  // This specifies the model to be used for generating embeddings
});
const embedding = openaiResponse.data[0].embedding;  // Extract the embedding vector from the response

// Perform a vector search in the 'ChatbotDataset' collection in the Qdrant database using the generated embedding
const searchResult = await qdrant_client.search("ChatbotDataset", {
  vector: embedding,  // Query vector
  limit: 10,  // Number of search results to return
});

// Output the search results
console.log("Search Results:");
for (const result of searchResult) {
    console.log(result.payload);  // Print the payload of each search result
}
console.log("-----------------------------------");  // Print a separator line for clarity
