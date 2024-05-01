/**
 * This file contains the main logic for the simple chat UI.
 * It creates a chat interface and handles user input.
 * It also listens for the GitHub link submission event and sets the link. 
 * This is a modified version of the example that WebLLm has on their github repo (why reinvent the wheel).
 * 
 * To view logs, open the browser console, CURRENLY THE WEBSCRAPED MODEL IS THROWING A BUNCH BUT THEY ARE NOT MISSION CRITICAL, IF
 * YOU HAVE THE TIME YOU COULD FIX THEM BUT ITS NOT NESSESARY SCROLL TO THE BOTTOM OF THE ERRORS TO FIND THE LOGS.
 * 
 * @author Christopher Mata
 * @version 1.1
 */

// Importing the necessary modules and our model registry
import appConfig from "./modelConfig";
import dotenv from 'dotenv'; 
import { ChatInterface, ChatModule, ChatRestModule, ChatWorkerClient, AppConfig } from "@mlc-ai/web-llm";

//Getting the enviornment ready
dotenv.config();

// Makes sure the element exists and returns it to be set as a variable
function getElementAndCheck(id: string): HTMLElement {
  const element = document.getElementById(id);
  if (element == null) {
    throw Error("Cannot find element " + id);
  }
  return element;
}

/**
 * Since webllm deals with browser cache, we need to make an object to house the chat UI within the cache
 */
class ChatUI {

  // Sets teh variables for the chat UI object
  private uiChat: HTMLElement;
  private uiChatInput: HTMLInputElement;
  private chat: ChatInterface;
  private localChat: ChatInterface;
  private config: AppConfig = appConfig;
  private selectedModel: string;
  private chatLoaded = false;
  private requestInProgress = false;
  // We use a request chain to ensure that
  // all requests send to chat are sequentialized
  private chatRequestChain: Promise<void> = Promise.resolve();
  private firebaseFunctionUrl: string;

  // Static variables to hold the github link and user prompt, without them, the chat UI will not get the proper data to initialize and work with.
  private static githubLink: string;
  private static userprompt: string;

  /**
   * Private constructor to ensure singleton pattern and for initialization of the browser cache object
   */
  private constructor() {
  }

  /**
   * An asynchronous factory constructor since we need to await getMaxStorageBufferBindingSize();
   * this is not allowed in a constructor (which cannot be asynchronous).
   * This method also sets up what we need by connecting UI elements and setting up the UI to work with the logic
   * 
   * @param chat The chat interface that will be used to generate the chat
   * @param localChat The chat interface that will be used to generate the chat locally, not generally needed but webllm requires it
   * @returns chatUI The chat UI object that is ready to be used
   */
  public static CreateAsync = async (chat: ChatInterface, localChat: ChatInterface) => {

    // The core of webllm
    const chatUI = new ChatUI();
    
    // use web worker to run chat generation in background
    chatUI.chat = chat;
    chatUI.localChat = localChat;


    // get the elements
    chatUI.uiChat = getElementAndCheck("chatui-chat");
    chatUI.uiChatInput = getElementAndCheck("chatui-input") as HTMLInputElement;

    // register event handlers, if you can think of anymore add them here! 
    getElementAndCheck("chatui-reset-btn").onclick = () => {
      chatUI.onReset();
    };
    getElementAndCheck("chatui-send-btn").onclick = () => {
      chatUI.onGenerate();
    };
    getElementAndCheck("chatui-input").onkeypress = (event) => {
      if (event.keyCode === 13) {
        chatUI.onGenerate();
      }
    };

    // When we detect low maxStorageBufferBindingSize, we assume that the device (e.g. an Android
    // phone) can only handle small models and make all other models unselectable. Otherwise, the
    // browser may crash. See https://github.com/mlc-ai/web-llm/issues/209.
    // Also use GPU vendor to decide whether it is a mobile device (hence with limited resources).
    const androidMaxStorageBufferBindingSize = 1 << 27;  // 128MB
    const mobileVendors = new Set<string>(["qualcomm", "arm"])
    let restrictModels = false;
    let maxStorageBufferBindingSize: number;
    let gpuVendor: string;
    try {
      [maxStorageBufferBindingSize, gpuVendor] = await Promise.all([
        chat.getMaxStorageBufferBindingSize(),
        chat.getGPUVendor(),
      ]);
    } catch (err) {
      chatUI.appendMessage("error", "Init error, " + err.toString());
      console.log(err.stack);
      return;
    }
    if ((gpuVendor.length != 0 && mobileVendors.has(gpuVendor)) ||
      (maxStorageBufferBindingSize <= androidMaxStorageBufferBindingSize)) {
      chatUI.appendMessage("init", "Your device seems to have " +
        "limited resources, so we restrict the selectable models.");
      restrictModels = true;
    }

    // Populate modelSelector AKA the dropdown menu
    const modelSelector = getElementAndCheck("chatui-select") as HTMLSelectElement;
    for (let i = 0; i < chatUI.config.model_list.length; ++i) {
      const item = chatUI.config.model_list[i];
      const opt = document.createElement("option");
      opt.value = item.local_id;
      opt.innerHTML = item.local_id;
      opt.selected = (i == 0);
      if (restrictModels && (item.low_resource_required === undefined || !item.low_resource_required)) {
        const params = new URLSearchParams(location.search);
        opt.disabled = !params.has("bypassRestrictions");
        opt.selected = false;
      }
      if (!modelSelector.lastChild?.textContent?.startsWith(opt.value.split('-')[0])) {
        modelSelector.appendChild(document.createElement("hr"));
      }
      modelSelector.appendChild(opt);
    }
    modelSelector.appendChild(document.createElement("hr"));

    // Append local server option to the model selector
    //NOTE: THis code is commented out because we do not want to use the local server, if you decide you want to use it, uncomment this code and you will
    // be all set to go.
    //const localServerOpt = document.createElement("option");
    //localServerOpt.value = "Local Server";
    //localServerOpt.innerHTML = "Local Server";
    //modelSelector.append(localServerOpt);

    // Set the selected model
    chatUI.selectedModel = modelSelector.value;
    modelSelector.onchange = () => {
      chatUI.onSelectChange(modelSelector);
    };

    return chatUI;
  }
  

  /**
   * Push a task to the execution queue. Allows tasks to be executed sequentially.
   *
   * @param task The task to be executed
   */
  private pushTask(task: () => Promise<void>) {
    const lastEvent = this.chatRequestChain;
    this.chatRequestChain = lastEvent.then(task);
  }

  /**
   * Event handlers
   * all event handler pushes the tasks to a queue
   * that get executed sequentially
   * the tasks previous tasks, which causes them to early stop
   * can be interrupted by chat.interruptGenerate
   * 
   * @returns exits the chat when conditions are met to ensure that resources are not being wasted
   */
  private async onGenerate() {
    if (this.requestInProgress) {
      return;
    }
    this.pushTask(async () => {
      await this.asyncGenerate();
    });
  }

  /**
   * When the user wants a different LLM model or Chat instance, this function is called to load the new model
   * 
   * @param modelSelector the selected model from the dropdown menue or advanced settings
   */
  private async onSelectChange(modelSelector: HTMLSelectElement) {
    if (this.requestInProgress) {
      // interrupt previous generation if any
      this.chat.interruptGenerate();
    }
    // try reset after previous requests finishes
    this.pushTask(async () => {
      await this.chat.resetChat();
      this.resetChatHistory();
      await this.unloadChat();
      this.selectedModel = modelSelector.value;
      await this.asyncInitChat();
    });
  }

  /**
   * Reset the chat when the reset button is clicked
   */
  private async onReset() {
    if (this.requestInProgress) {
      // interrupt previous generation if any
      this.chat.interruptGenerate();
    }
    // try reset after previous requests finishes
    this.pushTask(async () => {
      await this.chat.resetChat();
      this.resetChatHistory();
    });
  }

  /**
   * Internal function to append a message to the chat bubbles, its also attributes the message kind
   * 
   * @param kind Indicates the type of message 
   * @param text the text that will be displayed in the chat
   */
  private appendMessage(kind, text) {
    if (kind == "init") {
      text = "[System Initalize] " + text;
    }
    if (this.uiChat === undefined) {
      throw Error("cannot find ui chat");
    }
    if (kind == "info") {
      text = "[Info] " + text;
    }

    const msg = `
      <div class="msg ${kind}-msg">
        <div class="msg-bubble">
          <div class="msg-text">${text}</div>
        </div>
      </div>
    `;
    this.uiChat.insertAdjacentHTML("beforeend", msg);
    this.uiChat.scrollTo(0, this.uiChat.scrollHeight);
  }

  /**
   * This function updates the last message in the chat and displays it to the user
   * 
   * @param kind Inidicates the type of message
   * @param text The text that will be displayed in the chat
   * @returns The updated message
   */
  private updateLastMessage(kind, text) {

    //sees if the message is an init message
    if (kind == "init") {
      text = "[System Initalize] " + text;
    }
    if (this.uiChat === undefined) {
      throw Error("cannot find ui chat");
    }

    // gets the HTML elements and preps them for the new message
    const matches = this.uiChat.getElementsByClassName(`msg ${kind}-msg`);
    if (matches.length == 0) throw Error(`${kind} message do not exist`);
    const msg = matches[matches.length - 1];
    const msgText = msg.getElementsByClassName("msg-text");
    if (msgText.length != 1) throw Error("Expect msg-text");
    if (msgText[0].innerHTML == text) return;
    const list = text.split('\n').map((t) => {
      const item = document.createElement('div');
      item.textContent = t;
      return item;
    });

    // clear the message and update it with the new message 
    msgText[0].innerHTML = '';
    list.forEach((item) => msgText[0].append(item));
    this.uiChat.scrollTo(0, this.uiChat.scrollHeight);
  }
  
  /**
   * Reset the chat history used by the async method
   * The reason why they are seperated is for simplicity, allowing it to be async, and to ensure that the chat history is reset properly.
   * It adds the tags tags to messages so that they can be displayed or removed from the chat.
   */
  private resetChatHistory() {
    const clearTags = ["left", "right", "init", "error", "info"];
    for (const tag of clearTags) {
      // need to unpack to list so the iterator don't get affected by mutation
      const matches = [...this.uiChat.getElementsByClassName(`msg ${tag}-msg`)];
      for (const item of matches) {
        this.uiChat.removeChild(item);
      }
    }
  }

  /**
   * Initialize the chat asynchronously with the selected model and adds developer user notes to the chat
   * 
   * @returns exits the chat when conditions are met to ensure that resources are not being wasted
   */
  private async asyncInitChat() {

    // Checks if the chat is already loaded
    if (this.chatLoaded) return;
    this.requestInProgress = true;
    this.appendMessage("init", "");

    // Callback function to update the user on the progress of the chat
    const initProgressCallback = (report) => {
      this.updateLastMessage("init", report.text);
    }

    // Initialize the chat and set the developer notes MODIFY THIS IF YOU NEED TO TELL THE USER SOMETHING
    this.appendMessage("info", "Welcome to UWP Chatbot! \n\n Here are some things to know:");
    this.appendMessage("info", "1. Switch between chats in the dropdown or customize settings by clicking the top button (ONLY DO THIS IF YOU KNOW WHAT YOU ARE DOING). If issues arise, refresh the page or use the refresh button.");
    this.appendMessage("info", "2. Reset the chat anytime by clicking the reset button or refresh page. If you start typing without selecting a chat, refrain from deleting the message until displayed. " + 
      " If 'generating' appears, your question is being answered. Type another question when the input text changes. Once loading is complete (top-most system bubble), start chatting!");
    
    // Set the callback function to update the user on the progress of the chat 
    this.chat.setInitProgressCallback(initProgressCallback);

    // Try to initialize the chat with the selected model there is a mini model registry in here to help the user with advanced settings
    // THE REASON THE ADVANCED SETTINGS ARE IMPLEMNTED THIS WAY IS BECAUSE WEBLLM LOADS THEM FROM THE GITHUB LINK!
    try {
      if(ChatUI.githubLink != undefined) {
        const customAppConfig: AppConfig = {
          model_list: [
            {
              "model_url": "https://huggingface.co/mlc-ai/Mistral-7B-Instruct-v0.2-q4f16_1-MLC/resolve/main/",
			        "local_id": "custom settings model",
			        "model_lib_url": ChatUI.githubLink,
			        "vram_required_MB": 6079.02,
			        "low_resource_required": false,
			        "required_features": ["shader-f16"],
            }
          ]
        }

        console.log("$ - Greetings from async Chat GitHub link provided: " + ChatUI.githubLink);
        await this.chat.reload("custom settings model", undefined, customAppConfig);
        
      } else if (this.selectedModel != "Local Server") {
        await this.chat.reload(this.selectedModel, undefined, this.config);
      }
    } catch (err) {
      this.appendMessage("error", "Init error, " + err.toString());
      console.log(err.stack);
      this.unloadChat();
      this.requestInProgress = false;
      return;
    }
    this.requestInProgress = false;
    this.chatLoaded = true;
  }

  /**
   * Unload the chat asynchronously
   * 
   * @returns exits the chat when conditions are met to ensure that resources are not being wasted
   */
  private async unloadChat() {
    await this.chat.unload();
    this.chatLoaded = false;
  }

  /**
   * Runs the generation of the chat asynchronously
   */
  private async asyncGenerate() {
    await this.asyncInitChat();
    this.requestInProgress = true;
    const prompt = this.uiChatInput.value;
    ChatUI.userprompt = prompt;
    if (prompt == "") {
      this.requestInProgress = false;
      return;
    }

    // Updating the message box to show that the chat is generating
    this.appendMessage("right", prompt);
    this.uiChatInput.value = "";
    this.uiChatInput.setAttribute("placeholder", "Generating...");

    // Waits for the interaction with the firebase function to finish
    await this.firebaseFunctionCall(prompt);

    // Updating the chat
    this.appendMessage("left", "");
    const callbackUpdateResponse = (step, msg) => {
      this.updateLastMessage("left", msg);
    };

    // This is for local servers, If commented out, webllm complains so its here incase you want to use an external server rather than running it on the
    // users browser. Look at the LangChainAgent folder if you want a example of how to set up the server.
    try {
      if (this.selectedModel == "Local Server") {
        const output = await this.localChat.generate(ChatUI.userprompt, callbackUpdateResponse);
        this.updateLastMessage("left", output);
      } else {
        await console.log("$ - Greetings from sending prompt: " + ChatUI.userprompt);
        const output = await this.chat.generate(ChatUI.userprompt, callbackUpdateResponse);
        this.updateLastMessage("left", output);
      }
    } catch (err) {
      this.appendMessage("error", "Generate error, " + err.toString());
      console.log(err.stack);
      await this.unloadChat();
    }
    this.uiChatInput.setAttribute("placeholder", "Enter your message...");
    this.requestInProgress = false;
  }

  /**
   * This calls the firebase function to interact with the Qdrant database, look in the firebasefunction or this readme for more info
   * sends a POST request to it and gets a reponse back, if the response is not ok, it will log the error and tell the user to answer the first question
   * It sets the global userprompt variable to use in the chat
   * 
   * @param prompt The prompt that the user wants to ask the chatbot
   */
 public async firebaseFunctionCall(prompt: string) {

  // The URL of the firebase function and the data that will be sent to it
  const firebaseFunctionUrl = process.env.FIREBASE_LINK_FUNCTION!;
  const sendingData = {'prompt': prompt};

  console.log("$ - " + JSON.stringify(sendingData));

  // Sends a POST request to the firebase function
  try {
    const response = await fetch(firebaseFunctionUrl, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json'
    },
    body: JSON.stringify(sendingData)
    });

    // If the response is ok, it will log the response and extract the first payload from the response
    const responseData = await response.json();
    console.log("$ - Response body:", responseData);

    // If the response contains a prompt, it will extract the first payload and the text within the payload
    if ('prompt' in responseData) {
      console.log("Prompt:", responseData['prompt']);

      // Extracting the first payload
      const firstPayload = responseData.prompt[0].payload;

      // Accessing the text within the payload
      const payloadText = firstPayload.text;

      ChatUI.userprompt = "Here is the question the user wants If its illegal do not answer: " + prompt + ". Please answer the 1st question mentioned as a UWParkside Chatbot with the following data as a response, " +
        "ignore any other questions in the current prompt beyond this point: " + payloadText;

      console.log("$ - Modified prompt: " + ChatUI.userprompt);
    }
  } catch (error) {
    console.error("$ - An error occurred:", error);
    ChatUI.userprompt = "Please answer the question as a UWParkside Chatbot. Do not asnwer homework problems or state anythin illegal " + prompt;

    console.log("$ - Modified prompt: " + ChatUI.userprompt);
    }
  }

  /**
   * A quick URL validator to see if the URL is valid or not, IGNORE THE INITIAL CONSOLE LOG IT THROWS IN THE BROWSER CONSOLE ITS BECAUSE
   * IT IS A ASYNC METHOD THAT IT GETS CALLED INITIALLY
   * 
   * @param link Link to the github repo that contains the custom model settings the user provides
   */
  public static async setGitHubLink(link: string) {

    const githubRegex = /^https:\/\/raw\.githubusercontent\.com\/([a-zA-Z0-9-]+)\/([a-zA-Z0-9-_]+)\/.*\.wasm$/;

    if (!githubRegex.test(link) || !link.includes("Mistral-7B") || !link.endsWith(".wasm")) {
      alert("Invalid GitHub link. Refresh the page and please provide a valid GitHub link");
    } else {
      alert("GitHub link provided successfully!"
      + " Please enter a new message to the chat to load your settings. If something goes wrong refresh the page."
      + " If you no longer want to use the custom settings, refresh the page and provide a different setting or select a default chat.");
      ChatUI.githubLink = link;
    }
    console.log("$ - Greetings from setGitHubLink GitHub link provided: " + ChatUI.githubLink);
  }
}
 /**
  * Now that we exited the class, we can now call the class to create the ChatUI and logic as soon as the browser loads the page
  */

// Initilizes a webworker to run the chat in the background and sets up the chat UI
const useWebWorker = appConfig.use_web_worker;
let chat: ChatInterface;
let localChat: ChatInterface;

// If the web worker is used, the chat will be run in the background
if (useWebWorker) {
  chat = new ChatWorkerClient(new Worker(
    new URL('./worker.ts', import.meta.url),
    { type: 'module' }
  ));
  localChat = new ChatRestModule();
} else {
  chat = new ChatModule();
  localChat = new ChatRestModule();
}

// Sends the chat and local chat to the ChatUI to create the chat interface
ChatUI.CreateAsync(chat, localChat);


// Define the event listener function
function handleGitHubLinkSubmitted(event: CustomEvent<string>) {
  const link = event.detail;
  ChatUI.setGitHubLink(link);
}

// Add the event listener to the document to interact with the chatui.js in the behaviors folder
document.addEventListener('githubLinkSubmitted', handleGitHubLinkSubmitted as EventListener);
