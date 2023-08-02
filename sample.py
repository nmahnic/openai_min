import os
import openai
import pandas as pd
from pathlib import Path
from dotenv import load_dotenv

config_path_name = "./data/config.json"
prompt_path_name = "./data/prompt.txt"
output_path_name = "./data/output.txt"
output_path = Path(output_path_name)

if output_path.is_file():
    os.remove(output_path)


config_file = pd.read_json(open(config_path_name, "rb"))

parameters = config_file["parameters"]

output_format = parameters["output_format"]
temperature = parameters["temperature"]
engine = parameters["engine"]
main_context = parameters["main_context"]
print("output_format: ",output_format)
print("temperature: ",temperature)
print("engine: ",engine)
print("main_context: ",main_context)

prompt_file = open(prompt_path_name, "r")
prompt = prompt_file.read()
prompt_file.close()
print("PROPMT:") 
print(prompt)

load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = api_key

system_context = "Context:"+main_context+"\nOutput:"+output_format
print("SYSTEM_CONTEXT:")
print(system_context)
        
response=openai.ChatCompletion.create(
    model=engine,
    temperature=temperature,
    messages=[
        {"role": "system", "content": system_context },
        {"role": "user", "content": prompt},
    ]
)
answer = response["choices"][0]["message"]["content"]
print(answer)

with open(output_path_name, "w") as f:
    f.write(answer)