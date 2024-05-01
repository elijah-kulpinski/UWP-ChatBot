/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */

/**
 * Import function triggers from their respective submodules:
 *
 * import {onCall} from "firebase-functions/v2/https";
 * import {onDocumentWritten} from "firebase-functions/v2/firestore";
 *
 * See a full list of supported triggers at https://firebase.google.com/docs/functions
 */
// Start writing functions
// https://firebase.google.com/docs/functions/typescript

/** 
 * This file contains code for firebase functions to abstract away from the embedded model.
 * Here is a list of the current functions:
 * 1. qdrantQuery - This function takes a prompt and returns the top 3 most similar prompts from the dataset. 
 * 
 * @author Brandon Padjent
 * @author Christopher Mata
 * @version 1.0
 */

// Import the necessary libraries
import {onRequest} from "firebase-functions/v2/https";
import * as logger from "firebase-functions/logger";
import {OpenAI} from "openai";
import {QdrantClient} from "@qdrant/js-client-rest";

// Set the API keys for the OpenAI and Qdrant clients
//NOTE: CURRENTLY SET TO DUMMY VALUES, REFER TO THE RESPECTIVE README's FOR GETTING A VALID KEY
const openAIkey = "ab-234567890123456789012345678901234567890123456789012";
const qdrantKey = "https://random-url.us-east4-0.gcp.cloud.qdrant.io:0000";
const qdrantURL = "ab234567890123456789012345678901234567890123456789012";

// Create the onRequest function for the qdrantQuery and stores it in a variable
const qdrantQuery = onRequest({cors: true}, async (request, response) => {

  // Grabs the prompt from the request body and checks if it the prompt exists
  const prompt = request.body.prompt;
  if (!prompt) {
    logger.info("$ - Request" + JSON.stringify(request.body));
    response.status(400).send("No prompt field in the request");
    return;
  }

  // Logs the prompt to the firebase console
  logger.info("$ - Hello logs!: " + prompt, {structuredData: true});

  // Creates a new OpenAI client and Qdrant client
  const openaiClient = new OpenAI({
    apiKey: openAIkey,
  });
  const qdrantClient = new QdrantClient({
    url: qdrantKey,
    apiKey: qdrantURL, 
  });

  // Creates embeddings for the prompt and searches the generated vector against the database and retursn the 3 most similar entries.
  try {
    const openaiResponse = await openaiClient.embeddings.create({
      input: prompt,
      model: "text-embedding-3-small",
    });

    const embedding = openaiResponse.data[0].embedding;

    const searchResult = await qdrantClient.search("ChatbotDataset", {
      vector: embedding,
      limit: 3,
    });

    // prints the results of the query to the firebase console
    console.log("$ - Search Results:");
    for (const result of searchResult) {
      logger.info(result.payload);
    }

    response.send({message: "$ - Qdrant Response", prompt: searchResult});
  } catch (error) {
    console.error("$ - Error occurred:", error);
    response.status(500).send("Internal Server Error");
  }
});

// Exports any functions made in this file to firebase for deployment
export {qdrantQuery};