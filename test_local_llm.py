# Import the required libraries:
from langchain.prompts import PromptTemplate
from langchain_community.llms import CTransformers

## Function To get response from LLAma 2 model
blog_style='Researchers'
input_text='Machine Learning'
no_words=2000


def getLLamaresponse(input_text,no_words,blog_style):

    ### LLama2 model
    # llm=CTransformers(model='/home/priyanka/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin',
    #                   model_type='llama',
    #                   config={'max_new_tokens':4096,
    #                           'temperature':0.7})
    llm = CTransformers(model='/home/priyanka/Downloads/llama-2-7b-chat.ggmlv3.q8_0.bin',
                    model_type='llama',
                    config={'max_new_tokens': 1024, 'temperature': 0.7, 'context_length': 4096})

    ## Prompt Template

    

    template="""
        Write a blog for {blog_style} job profile for a topic {input_text}
        within {no_words} words.
            """
    
    prompt=PromptTemplate(input_variables=["blog_style","input_text",'no_words'],
                          template=template)
    
    ## Generate the ressponse from the LLama 2 model
    response=llm.invoke(prompt.format(blog_style=blog_style,input_text=input_text,no_words=no_words))
    print(response)
    return response


getLLamaresponse(input_text, no_words, blog_style )