/**
 * This file is the entry point for the web worker.
 * A webworker allows for scripts to run in the background without blocking the main thread.
 * This is a slightly modified version of the one webllm uses.
 * 
 * @Author Christopher Mata
 */

// Import the necessary modules
import { ChatWorkerHandler, ChatModule } from "@mlc-ai/web-llm";

// Create a new instance of the ChatModule and ChatWorkerHandler
const chat = new ChatModule();
const handler = new ChatWorkerHandler(chat);
self.onmessage = (msg: MessageEvent) => {
  handler.onmessage(msg);
};
