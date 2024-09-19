from langchain_huggingface import HuggingFaceEndpoint


import os
os.environ["HUGGINGFACEHUB_API_TOKEN"]=sec_key



repo_id="mistralai/Mistral-7B-Instruct-v0.3"
llm=HuggingFaceEndpoint(repo_id=repo_id,max_length=128,temperature=0.7,huggingfacehub_api_token=sec_key)

# Increase the timeout to handle longer load times
try:
    # Invoke the model with a question
    response = llm.invoke("What is machine learning", timeout=300)  # Increase timeout to 300 seconds
    print(response)
except Exception as e:
    print(f"Error: {e}")


# from transformers import AutoModelForCausalLM, AutoTokenizer
# from langchain_core.language_models import HuggingFacePipeline
# from transformers import pipeline

# # Load the local model and tokenizer
# model_name = "/home/priyanka/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin"  # Replace with the path to your local model
# tokenizer = AutoTokenizer.from_pretrained(model_name)
# model = AutoModelForCausalLM.from_pretrained(model_name)

# # Create a pipeline
# local_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

# # Wrap the pipeline in a Langchain-compatible LLM
# llm = HuggingFacePipeline(pipeline=local_pipeline)

# # Use the model for inference
# response = llm.invoke("What is machine learning?")
# print(response)