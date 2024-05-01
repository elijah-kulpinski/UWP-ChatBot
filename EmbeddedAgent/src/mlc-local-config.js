/**
 * Sample model Regestry with a list of currenly supported models. Please look at the WebLLM documentation to see how to add more models and currenly
 * supported models. THE DIFFERENCE IS THAT THIS IS FOR LOCAL MODELS IF YOU CHOOSE TO USE THEM, PLEASE MODIFY THIS FILE AND REPLACE THE OTHER MODEL REGESTRY
 * WITH IT IN THE simple_chat.ts FILE TO USE A LOCAL HOSTED MODEL IN A SERVER OF YOUR CHOOSING. 
 * 
 * This file came with webllm templates, please refer to the modelConfig.js for our current model registry.
 */

// config used when serving from local mlc-llm/dist
// use web-llm/script/serve_mlc_llm_dist.sh to start the artifact server
export default {
  "model_list": [
    {
      "model_url": "http://localhost:8000/RedPajama-INCITE-Chat-3B-v1-q4f32_1/params/",
      "local_id": "RedPajama-INCITE-Chat-3B-v1-q4f32_1",
      "model_lib_url": "http://localhost:8000/RedPajama-INCITE-Chat-3B-v1-q4f32_1/RedPajama-INCITE-Chat-3B-v1-q4f32_1-webgpu.wasm",
    },
    {
      "model_url": "http://localhost:8000/Llama-2-7b-chat-hf-q4f32_1/params/",
      "local_id": "Llama-2-7b-chat-hf-q4f32_1",
      "model_lib_url": "http://localhost:8000/Llama-2-7b-chat-hf-q4f32_1/Llama-2-7b-chat-hf-q4f32_1-webgpu.wasm",
    },
    // fp16 options are enabled through chrome canary flags
    // chrome --enable-dawn-features=enable_unsafe_apis
    {
      "model_url": "http://localhost:8000/RedPajama-INCITE-Chat-3B-v1-q4f16_1/params/",
      "local_id": "RedPajama-INCITE-Chat-3B-v1-q4f16_1",
      "model_lib_url": "http://localhost:8000/RedPajama-INCITE-Chat-3B-v1-q4f16_1/RedPajama-INCITE-Chat-3B-v1-q4f16_1-webgpu.wasm",
      "required_features": ["shader-f16"]
    }
  ],
  "use_web_worker": true
}
