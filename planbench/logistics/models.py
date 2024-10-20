import os
import openai
import backoff 
import time
completion_tokens = prompt_tokens = 0
from openai import AzureOpenAI

# api_key = os.getenv("OPENAI_API_KEY", "")
# if api_key != "":
#     openai.api_key = api_key
# else:
#     print("Warning: OPENAI_API_KEY is not set")
    
# api_base = os.getenv("OPENAI_API_BASE", "")
# if api_base != "":
#     print("Warning: OPENAI_API_BASE is set to {}".format(api_base))
#     openai.api_base = api_base

# @backoff.on_exception(backoff.expo, openai.APIError)
def completions_with_backoff(**kwargs):
    # return openai.ChatCompletion.create(**kwargs)
    another_cur_try = 0
    while another_cur_try <50:
        try:


            return client.chat.completions.create(**kwargs)
        except Exception as e:
            err = f"Error: {str(e)}"
            print(err)
            time.sleep(120)
            
            continue

def gpt(prompt,empty_response=0, engine="gpt-4-32k", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    if empty_response==0:

        messages = [{
            "role": "system",
            "content": "you are an AI assistant",
        }]
        messages.append({"role": "user", "content": prompt})
    else:
        messages = prompt


    return chatgpt(messages, engine=engine, temperature=temperature, max_tokens=max_tokens, n=n, stop=stop)
    
def chatgpt(messages, engine="gpt-4-32k", temperature=0.7, max_tokens=1000, n=1, stop=None) -> list:
    global completion_tokens, prompt_tokens
    outputs = []
    while n > 0:
        cnt = min(n, 20)
        n -= cnt
        time1=time.time()
        # res = completions_with_backoff(engine=engine, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        res = completions_with_backoff(model=deployment_name, messages=messages, temperature=temperature, max_tokens=max_tokens, n=cnt, stop=stop)
        
        time2=time.time()
        outputs.extend([choice.message.content for choice in res.choices])
        # log completion tokens
        completion_tokens += res.usage.completion_tokens
        prompt_tokens += res.usage.prompt_tokens
    return outputs,messages, res.usage.prompt_tokens, res.usage.completion_tokens,time2-time1
    
def gpt_usage(backend="gpt-4"):
    global completion_tokens, prompt_tokens
    if backend == "gpt-4":
        cost = completion_tokens / 1000 * 0.06 + prompt_tokens / 1000 * 0.03
    elif backend == "gpt-3.5-turbo":
        cost = completion_tokens / 1000 * 0.002 + prompt_tokens / 1000 * 0.0015
    return {"completion_tokens": completion_tokens, "prompt_tokens": prompt_tokens, "cost": cost}
