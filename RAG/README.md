# Creating a Qdrant Cluster Using the Free Tier

This guide provides detailed steps on how to set up a Qdrant cluster using the free tier. Qdrant is a vector search engine that supports fast similarity search for vectors with high-dimensional features.

## Step 1: Sign Up for Qdrant

To start using Qdrant, you need to first create an account:

- **Visit the Qdrant website**: Navigate to [Qdrant's website](https://qdrant.tech/) and proceed to the sign-up or registration page.
- **Create an account**: Complete the registration form with your details such as email and password, or use an existing Google or GitHub account to sign up.
- **Verify your account**: Follow the verification link sent to your email to activate your account.

## Step 2: Access the Qdrant Console

Once registered, you can access the Qdrant console to manage your services.

- **Log in**: Enter your credentials to log into the Qdrant console.
- **Dashboard**: This is where you'll manage your clusters and interact with Qdrant services.

## Step 3: Create a New Cluster

Here's how to create a new cluster in the Qdrant console:

- **Cluster Management**: Navigate to the “Clusters” section in the console.
- **Create a Cluster**: Click on “Create Cluster” or a similar button.
- **Choose the Free Tier**: Select the free tier option, keeping in mind it may have certain limitations.
- **Configure Your Cluster**: Fill in the necessary details:
  - **Cluster Name**: Give your cluster a unique name.
  - **Region**: Choose the region closest to you to reduce latency.
  - **Node Type and Size**: The free tier will have predefined options here.

- **Launch the Cluster**: After configuring the settings, start your cluster. It might take a few minutes to initialize.

## Step 4: Configure Your Cluster

Configure your cluster for optimized performance and security:

- **Access Control**: Set up necessary API keys or manage access controls if available.
- **Create Collections**: You need to create collections before indexing vectors:
  - **Collections Tab**: Go to this tab to manage collections.
  - **New Collection**: Define parameters like name, vector size, and distance metric (e.g., Euclidean, Cosine).
  - **Helpful Script**: You can utilize CreateCollection.py for creating/viewing/deleting collections.

## Step 5: Connect to Your Cluster

With your cluster ready, integrate it with your applications:

- **Connection Details**: Note down the cluster URL and any API keys.
- **Integrate**: Use Qdrant client libraries to connect your application to the cluster. Initialization typically requires the URL and API key:
  - **Populating the Cluster**: You can enter data into a collection using the DatasetToQdrant.py script.
  - **Query the Cluster**: You can query data from a collection using the QdrantQuery.mjs script. It is written in typescript for use in frontend.

# Spring 2024 Setup

Data from Dataset.txt was loaded into a Qdrant cluster named "ChatbotDataset" using the

#### Dataset.txt
This dataset is from after the dataset was cleaned but before it was expanded. The expanded dataset has several variations of the same answer to teach the models different ways to "talk" but this is not necessary for the database, we just want the data.

#### DatasetToQdrant.py
Given the size of the dataset, this script has been setup to create and upload embeddings for 100 lines at a time. Additionally, some lines are longer than what the "text-embedding-3-small" model supports. You may want to review the Qdrant and OpenAI documentation to see if an improved model is available, the choice of using the small model is to remain cost effective. If the OpenAI call to create the embedding raises an error then the line is skipped and the line number is printed to the console. After 100 lines have been embedded they are inserted into the qdrant collection, then the loop moves to the next 100. Note that the script will take some time to run as it is limited by the speed of the API calls.

If you do not have access to OpenAi, you can also use a custom model from HuggingFace. In order to use a custom model you will need to have a server setup to handle the query as whichever model is used to vectorize the dataset will also need to be used to query the collection.

One alternative our group had briefly considered was using the WebLLM model to create the vectors on the frontend, then those vectors would be used in the query run by firebase. Again, the model used to query must be the same as the one used to vectorize the dataset. Because our group was utilizing several different models as options on the front end, this was not practical for us. You could get around this by having a separate collection for each model available to the users, then when running the query it would query the collection associated with the model used. Depending on the size of your dataset having multiple copies of it in qdrant may consume much of the free tier.

#### CreateCollection.py
This script includes commands for creating, deleting, and viewing collections in your Qdrant cluster. You must ensure the collection_name matches across all scripts unless using multiple collections, I used the name ChatbotDataset. There are purposes in having multiple collections, however those did not apply to us at the time of writitng. If you would like to utilize multiple collections simply run the create collection line with a different name as the existing collection(s). Qdrant has documentation on the uses and purposes of having multiple collections.

#### QdrantQuery.mjs
This is the code used in firebase to query the database. It is written in Typescript for compatability, if you would like a query script for testing, Qdrant has example query scripts written in python. The variable "text" is what you can use to test the query functionality. You must ensure that the model matches the model used for embedding the dataset. In this case because I used OpenAi I have an OpenAi API call to create an embedding of the text using the text-embedding-3-small model. OpenAi has other models available however this one is the most cost effective at the time of writing.
