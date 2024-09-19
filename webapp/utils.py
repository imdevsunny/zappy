# utils.py
from langchain_community.llms import CTransformers

class ModelSingleton:
    _instance = None

    @staticmethod
    def get_instance():
        if ModelSingleton._instance is None:
            ModelSingleton()
        return ModelSingleton._instance

    def __init__(self):
        if ModelSingleton._instance is not None:
            raise Exception("This class is a singleton!")
        else:
            # Initialize the model
            self.llm = CTransformers(
                model='/home/priyanka/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin',
                model_type='llama',
                config={'max_new_tokens': 1024, 'temperature': 0.7, 'context_length': 4096}
            )
            ModelSingleton._instance = self

    def get_llm(self):
        return self.llm
