/**
 * Our current model regestry in the simple_chat.ts file. With the current models we have available for use.
 * IF OUR OWN MODEL IS NOT ADDED HERE YET  (If your seeing the all caps its not implemented yet) PLEASE REFER TO THE MODEL TRAINING DOCUMENTATION
 * TO ADD IT WITH THE WEBLLM DOCUMENTATION.
 * 
 * @author Christopher Mata
 */
export default {
	"model_list": [

		// Initiall Chat Message and loads this model if the user does not select from the dropdown and starts typing
		{
			"model_url": "https://huggingface.co/mlc-ai/Mistral-7B-Instruct-v0.2-q4f16_1-MLC/resolve/main/",
			"local_id": "Click to select a chat or start typing!",
			"model_lib_url": "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/Mistral-7B-Instruct-v0.2/Mistral-7B-Instruct-v0.2-q4f16_1-sw4k_cs1k-webgpu.wasm",
			"vram_required_MB": 6079.02,
			"low_resource_required": false,
			"required_features": ["shader-f16"],
		},

		// Mistral variants
		{
			"model_url": "https://huggingface.co/mlc-ai/Mistral-7B-Instruct-v0.2-q4f16_1-MLC/resolve/main/",
			"local_id": "Mistral-7B-Instruct-v0.2-q4f16_1",
			"model_lib_url": "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/Mistral-7B-Instruct-v0.2/Mistral-7B-Instruct-v0.2-q4f16_1-sw4k_cs1k-webgpu.wasm",
			"vram_required_MB": 6079.02,
			"low_resource_required": false,
			"required_features": ["shader-f16"],
		},
		// Phi-2
		{
			"model_url": "https://huggingface.co/mlc-ai/phi-2-q0f16-MLC/resolve/main/",
			"local_id": "Phi2-q0f16",
			"model_lib_url": "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/phi-2/phi-2-q0f16-ctx2k-webgpu.wasm",
			"vram_required_MB": 11079.47,
			"low_resource_required": false,
			"required_features": ["shader-f16"],
		},
		{
			"model_url": "https://huggingface.co/mlc-ai/phi-2-q4f16_1-MLC/resolve/main/",
			"local_id": "Phi2-q4f16_1",
			"model_lib_url": "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/phi-2/phi-2-q4f16_1-ctx2k-webgpu.wasm",
			"vram_required_MB": 3053.97,
			"low_resource_required": false,
			"required_features": ["shader-f16"],
		},
		{
			"model_url": "https://huggingface.co/mlc-ai/phi-2-q4f16_1-MLC/resolve/main/",
			"local_id": "Phi2-q4f16_1-1k",
			"model_lib_url": "https://raw.githubusercontent.com/mlc-ai/binary-mlc-llm-libs/main/phi-2/phi-2-q4f16_1-ctx1k-webgpu.wasm",
			"vram_required_MB": 2131.97,
			"low_resource_required": true,
			"required_features": ["shader-f16"],
		},
	],
	"use_web_worker": true
}
