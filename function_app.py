import azure.functions as func
import logging
import os
from openai import AzureOpenAI
from langchain.prompts import PromptTemplate
# from langchain_openai import OpenAI
# from langchain_openai import AzureOpenAI

app = func.FunctionApp()

@app.function_name(name='ask')
@app.route(route='ask', auth_level='anonymous', methods=['POST'])
def main(req):

    prompt = req.params.get('prompt') 
    if not prompt: 
        try: 
            req_body = req.get_json() 
        except ValueError: 
            raise RuntimeError("prompt data must be set in POST.") 
        else: 
            prompt = req_body.get('prompt') 
            if not prompt:
                raise RuntimeError("prompt data must be set in POST.")

    # init OpenAI: Replace these with your own values, either in environment variables or directly here
    USE_LANGCHAIN = os.getenv("USE_LANGCHAIN", 'True').lower() in ('true', '1', 't')
    AZURE_OPENAI_API_KEY = os.environ.get("AZURE_OPENAI_API_KEY")
    AZURE_OPENAI_ENDPOINT = os.environ.get("AZURE_OPENAI_ENDPOINT")
    AZURE_OPENAI_SERVICE = os.environ.get("AZURE_OPENAI_SERVICE") or "myopenai"
    AZURE_OPENAI_GPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_GPT_DEPLOYMENT") or "davinci"
    AZURE_OPENAI_CHATGPT_DEPLOYMENT = os.environ.get("AZURE_OPENAI_CHATGPT_DEPLOYMENT") or "chat" #GPT turbo
    if 'AZURE_OPENAI_API_KEY' not in os.environ:
        raise RuntimeError("No 'AZURE_OPENAI_API_KEY' env var set.  Please see Readme.")

    # configure azure openai for langchain and/or llm
    # openai.api_key = AZURE_OPENAI_API_KEY
    # openai.api_base = AZURE_OPENAI_ENDPOINT # your endpoint should look like the following https://YOUR_RESOURCE_NAME.openai.azure.com/
    # openai.api_type = 'azure'
    # openai.api_version = '2023-05-15' # this may change in the future
    #                                   # for langchain, set this version in environment variables using OPENAI_API_VERSION
    api_version = "2023-05-15"


    if bool(False):
        # logging.info('Using Langchain')

        # llm = AzureOpenAI(deployment_name=AZURE_OPENAI_CHATGPT_DEPLOYMENT, temperature=0.3, openai_api_key=AZURE_OPENAI_KEY)
        # llm_prompt = PromptTemplate(
        #     input_variables=["human_prompt"],
        #     template="The following is a conversation with an AI assistant. The assistant is helpful.\n\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {human_prompt}?",
        # )
        # from langchain.chains import LLMChain
        # chain = LLMChain(llm=llm, prompt=llm_prompt)
        # return chain.run(prompt)
        return ""

    else:
        logging.info('Using ChatGPT LLM directly')

        # gets the API Key from environment variable AZURE_OPENAI_API_KEY
        client = AzureOpenAI(
            # https://learn.microsoft.com/en-us/azure/ai-services/openai/reference#rest-api-versioning
            api_version=api_version,
            # api_key=AZURE_OPENAI_API_KEY,
            # https://learn.microsoft.com/en-us/azure/cognitive-services/openai/how-to/create-resource?pivots=web-portal#create-a-resource
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            azure_deployment=AZURE_OPENAI_CHATGPT_DEPLOYMENT,  # e.g. gpt-35-instant
        )

        
        completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": "Say this is a test",
                }
            ],
            model=AZURE_OPENAI_CHATGPT_DEPLOYMENT, #ignored here, can be anything
        )
        print(completion.choices[0].message.content)
        return completion.to_json()


def generate_prompt(prompt):
    capitalized_prompt = prompt.capitalize()

    # Chat
    return f'The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: {capitalized_prompt}' 

    # Classification
    #return 'The following is a list of companies and the categories they fall into:\n\nApple, Facebook, Fedex\n\nApple\nCategory: ' 

    # Natural language to Python
    #return '\"\"\"\n1. Create a list of first names\n2. Create a list of last names\n3. Combine them randomly into a list of 100 full names\n\"\"\"'
