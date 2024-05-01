
# Firebase Functions

This folder contains everything related to Firebase functions! The current code and stubs here are using dummy API keys and URLs.

- Q: Now you might be asking why we need Firebase functions?
- A. Sometimes we need to make mini servers to get stuff done that cannot be done within a browser, so we make a simple function in Firebase to serve as our server. We also abstract away tasks so that the user would not experience any more performance hindrances.

## Additional Info About the folder
The functions folder has all the source code all the Firebase and source code things
- Open it up to see more folders

The Node modules folder has config libraries in there
- Please look at the project install section in this README

The src code folder has the source code
- add more Typescript files or add to the index.ts

## What is needed for the project

Software:
- Look in Project [README](https://github.com/uwp-se/ChatBot)

API/Libraries:
- [OpenAI](https://platform.openai.com)
- [Qdrant](https://qdrant.tech/)
- [FirebaseFunctions](https://firebase.google.com/docs/functions)

Keys/URL's:
Please obtain the following since they are set to dummy values in the code. Refer to [README](https://github.com/uwp-se/ChatBot/tree/master/RAG) for everything database related, use it to complete these functions.
- OpenAI
- QdrantAPI Key
- QdrantURL

Languages and other stuff
- TypeScript
- [PostMan](https://www.postman.com/) - Useful for debugging




## Installation and deployment

This is a comprehensive section dictating how to get Firebase functions to work! I am assuming you already did the steps in the project [README](https://github.com/uwp-se/ChatBot) AKA cloned the repo. I am also assuming you have also gathered the necessary API keys and URLs from their README. We are also under the assumption that you have node AKA npm installed on your machine. If you do not have node, refer to [EmbeddedAgent](https://github.com/uwp-se/ChatBot/tree/master/EmbeddedAgent)

cd into the directory and set up the environment, when in the parent ChatBot folder:
```bash
  cd FirebaseFunctions
  cd functions
```
THE FIRST THING is to set up the Firebase commands globally on your machine, run the following:
```bash
  npm install -g firebase-tools
```

THE SECOND THING YOU NEED TO DO IS LOG INTO YOUR FIREBASE ACCOUNT. The following logs the previous team's accounts out (just in case), and logs you in:
```bash
  firebase logout
  firebase login
```

If a node_modules folder does not exist or if it does not have any dependencies:
```bash
  npm install
```

When you replace the API keys and URL and are ready to deploy to your Firebase instance, run the following:
```bash
  firebase deploy
```

NOTE: It will take some time to deploy and you might get some errors. Those errors pertain to invalid keys (If you have the wrong one) or the most likely cause is the syntax of the TypeScript (Firebase is picky on the style in which you write). If this occurs to you, just look at the console and see what syntax errors it is complaining about. Once the deployment script lets you deploy, copy the URL it gives you and use it for the [EmbeddedAgents](https://github.com/uwp-se/ChatBot/tree/master/EmbeddedAgent) Environmental Variable called FIREBASE_LINK_FUNCTION :)

If you are still confused about how to set up Firebase functions here is a cool [video](https://youtu.be/DYfP-UIKxH0?si=dHPnN-XpFtpbEqBn) I have used for all my projects as a reference.


## HTTP request reference

#### POST to firebase functions:


| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `prompt` | `string` | **Required**. User message |

Example HTTP Request:
```HTTP
  POST https://firebasefunctionname-1234567-uc.a.run.app
```

#### RESPONSE to the client
| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `prompt`      | `none` | **Required**. Qdrant query results |
| `message` | `string` | **Optional**. Quick query status messages: success or failed |


## IDEAS for future team functions!

- Canvas Integration
- Outlook Integration
- Solar Integration
- Integration with other SE teams
- And More! The only limit to this project is your imagination!


## Authors - feel free to add your GitHub here if you worked on the project!

-  Qdrant functionality: [@Brandon Padjent](https://github.com/Jediscout27)
- Developer of the function structure/server dichotomy: [@Christopher Mata](https://github.com/Christopher-Mata)
