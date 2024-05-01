# EmbeddedAgent

This folder provides a complete implementation of a ChatBot based on [WebLLM](https://webllm.mlc.ai/). Please refernce it to add more features! Its a cool library that enables LLMs to run directly on the users device (or even in a browser) This readme will provide you with all the info needed to start developing! This is the current implementation and version of the ChatBot Project. The previous implementation used Langchain in the [LangchainAgent](https://github.com/uwp-se/ChatBot/tree/master/LangchainAgent) folder. WebLLm is dependent on browser cache btw.

WebLLM relies on [WebGPU](https://codelabs.developers.google.com/your-first-webgpu-app#0)some browsers support it out of the box and others dont, I suggest using Chrome since it supports it nativly.
LIST OF BROWSERS THAT SUPPORT WebGPU/WebLLM:
- [Chrome](https://www.google.com/chrome/)
- [Firefox nightly](https://wiki.mozilla.org/Nightly)
- More browsers are releasing them but at the time of making this doc, these are the only 2. Please look up more supported browsers

WebLLM is built upon MLC Chat
- [Docs for MLC Chat](https://llm.mlc.ai/)

For information on the webscrapping we did:
- [Github FrontEnd Website folder](https://github.com/uwp-se/ChatBot/tree/master/Frontend%20Website)

Although the Langchain agent is obselete because you can use WebLLM to also have a seperate server for LLM computation using the commented out code and a bit of modification to the existing code, we still keep it for a good reference.

Before working on this project, run it first via the instructions bellow so you can see how everything works! Look at the code within the files to find out more on the implementation. Also, here is the github link to test the custom settings feature: https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/Mistral-7B-Instruct-v0.2/Mistral-7B-Instruct-v0.2-q4f16_1-sw4k_cs1k-webgpu.wasm 

## Additional Info About the folder
The src folder has all the source code
- Within that src folder the app-config.js and gh-config.js and mlc-local-config.js are extra not used files for your refernce on the model regestry
- Within that src folder there is an img folder to contain the images used in the CSS and a behaviors folder which contains additional behaviors of the ChatUI window
- index.html = HTML of the webscraped website (Scroll all the way at the bottom to see our HTML on the chat app)
- llm_chat.css = Styling of the website
- simple_chat.ts = The main functionality of the embedded agent
- modelConfig.js = The current model registry
- chatui.js = controls additional popup windows and throws an event to be catched by simple_chat
- worker.ts = Allows for the chat to run as a background process

The Node modules folder has config libraries in there
- Please look at the project install section in this README

The .parcel-cache and dist folder NOTE: DELETE BOTH BETWEEN RUNS AND DEPLOYS
- .parcel-cache folder contains files to help it run
- dist folder contains the translated Typescript/JavaScript code to run

## What is needed for the project

Software:
- Look in Project [README](https://github.com/uwp-se/ChatBot)

API/Libraries:
- [WebLLM](https://webllm.mlc.ai/)
- [dotenv](https://www.npmjs.com/package/dotenv)
- [WebGPU](https://codelabs.developers.google.com/your-first-webgpu-app#0)
- [mlc](https://llm.mlc.ai/)
- [Parcel](https://parceljs.org/docs/)
- [node](https://nodejs.org/en/download)

Keys/URL's:
PLEASE LOOK AT THE ENVIRONMENT VARIABLES section futher down before running

Languages and other stuff
- TypeScript
- JavaScript
- CSS/HTML
- Knowlegde about HTTP Request
- Knowledge about npm and json


## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

`FIREBASE_LINK_FUNCTION`: Follow the steps in the FirebaseFunction [README](https://github.com/uwp-se/ChatBot/tree/master/FirebaseFunctions) to obtain this URL.


## Installation and deployment

This is a comprehensive section dictating how run the embedded client! I am assuming you already did the steps in the project [README](https://github.com/uwp-se/ChatBot). AKA cloned the repo. I am also assuming you have also gathared the nessesary API keys and URLS from their READMES.

- PLEASE REFERENCE [WEBLLM](https://webllm.mlc.ai/) DOCUMENTATION FOR FURTHER DEVELOPMENT

- Install [node](https://nodejs.org/en/download) on your machine
- Gather the FirebaseFunction URL from the FirebaseFunction[README](). 

cd into directory and set up the enviornment, when in the parant ChatBot folder:
```bash
  cd EmbeddedAgent
```

If a node_modules folder does not exist or if it does not have any dependencies:
```bash
  npm install
```

If everything is installed sucessfully you are ready to run it using:
```bash
  npm start
```

NOTE: To get TypeScript working with the webscraped website. I needed to wrap [parcel](https://parceljs.org/) a nice TypeScript translator within npm, so when you run "npm start" you are actually running the following
```json
"scripts": {
  "start": "parcel src/llm_chat.html --port 8888",
         "mlc-local": "parcel src/llm_chat.html --port 8888",
         "build": "parcel build src/llm_chat.html --dist-dir lib --no-content-hash"
}
```
As you can deduce from the top, there are 3 differnt scripts build compliles, mcl-local is there so the complier does not get mad, and start which will run the agent at [localhost port 8888](http://localhost:8888/)
## HTTP request reference (Same as the Firebase README)

#### POST TO FIREBASE FUNCTIONS:


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `prompt` | `string` | **Required**. User message |

#### Get item

For localhost
```http
  http://localhost:8888/
```

#### RESPONSE to the client
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `prompt`      | `none` | **Required**. Qdrant query results |
| `message` | `string` | **Optional**. Quick query status messages: success or failed |


## Deployment

To deploy the project to whichever hosting platform you choose, please do the following and reference [Parcel](https://parceljs.org/) documentation

```bash
  This example uses Firebase

  Run Command Prompt
  
  Install any required firebase tools with the line 'npm update -g firebase-tools'
  
  Type 'firebase login' to login to firebase (follow instructions to login)
  
  Then type 'firebase init' to begin initalization (follow instructions as needed)
  
  Once initialization is complete, type 'firebase deploy' to deploy the project
  
  When completed with no errors, two links will be provided
    Project Console: Will open the main Firebase Console for the Project deployed
    Hosting URL: The actual link of the project (in this example, it is 'https://chatbot-3a2b9.web.app/')
  
NOTE: The BLAZE plan was needed to deploy this project. Exact pricing for hosting/deploying varies from project to project. For more information on Firebase pricing, visit 'https://firebase.google.com/pricing'
```


## IDEAS for future teams!

Webllm allows for some wacky things to be made! Unfornutaly, the founding team only had time to implement everything for web :
- Make web side into React App if possilbe???
- Work on Qdrant Database a bit more
- Browser Extention
- IOS app
- Android app 
- Canvas Integration
- Outlook Integration
- Solar Inegration
- Integration with other SE teams
- And More! The only limit to this project is your imagination!
## Authors - fell free to add your GitHub here if you worked on the project!

- literally made 95% of the code in this folder: [@Christopher Mata](https://github.com/Christopher-Mata)
- Deployment: [Jose Giles](https://github.com/JoalChat2024)