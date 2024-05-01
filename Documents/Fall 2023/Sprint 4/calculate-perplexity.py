from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import load_dataset
import torch
from tqdm import tqdm  # for progress bar

def calculate_perplexity(model, tokenizer, text, stride, max_length):
    """
    Calculates the perplexity of the text using the given model and tokenizer.
    """
    encodings = tokenizer(text, return_tensors='pt')

    # Calculate the length of the sequence and define max_length if not provided
    seq_len = encodings.input_ids.size(1)
    max_length = max_length or model.config.max_position_embeddings

    nlls = []
    for begin_loc in tqdm(range(0, seq_len, stride), desc="Calculating Perplexity"):
        end_loc = min(begin_loc + max_length, seq_len)
        trg_len = end_loc - begin_loc
        input_ids = encodings.input_ids[:, begin_loc:end_loc]
        target_ids = input_ids.clone()
        target_ids[:, :-trg_len] = -100  # Mask out the non-target part of the input

        with torch.no_grad():
            outputs = model(input_ids=input_ids, labels=target_ids)
            nlls.append(outputs.loss * trg_len)

    # Calculate the average negative log likelihood and then the perplexity
    avg_nll = torch.stack(nlls).sum() / seq_len
    perplexity = torch.exp(avg_nll).item()
    return perplexity

def load_text_from_dataset(dataset_name):
    """
    Loads text from the specified dataset.
    """
    if dataset_name == 'wikitext-103':
        data = load_dataset('wikitext', 'wikitext-103-raw-v1', split='test')
        text = "\n\n".join(data['text'])
    else:
        raise ValueError("Unsupported dataset. Please add the dataset handling logic.")
    return text

def main():
    # Specify the dataset name here
    dataset_name = 'wikitext-103'
    text = load_text_from_dataset(dataset_name)
    
    # Define the model to use
    model_name = "Open-Orca/Mistral-7B-OpenOrca"
    
    # Load the model and tokenizer
    try:
        print(f"Loading model `{model_name}`...")
        model = AutoModelForCausalLM.from_pretrained(model_name).to('cuda')
        tokenizer = AutoTokenizer.from_pretrained(model_name)
    except Exception as e:
        print(f"An error occurred while loading the model: {e}")
        return
    
    # Define the stride and maximum length for processing the text
    stride = 1024
    max_length = model.config.max_position_embeddings
    
    # Calculate perplexity
    perplexity = calculate_perplexity(model, tokenizer, text, stride, max_length)
    print(f"The perplexity for `{model_name}` on `{dataset_name}` is: {perplexity}")

if __name__ == "__main__":
    main()
