"""
Ninja Django API to collect the
"""
import os, sys
from ninja import Router

import glob
from typing import List
from multiprocessing import Pool
from tqdm import tqdm
import subprocess

router = Router()

#TODO: update to add the argument for model_path
@router.get("/prompt_c")
def AIChat(request,input:str):
    llama2_bin = "/Users/ousheshharadhun/Documents/Workspace/FacebookLLAMA/LLM_Backup/llm_backend_go/Backend/manager/llama2.c/./run"
    llama2_model = "/Users/ousheshharadhun/Documents/Workspace/FacebookLLAMA/LLM_Backup/llm_backend_go/Backend/manager/llama2.c/stories15M.bin"

    cmd = [llama2_bin, llama2_model, "-t", "0.8", "-n", "256", "-i", input]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,text=True)

    output = []
    for line in iter(process.stdout.readline,""):
        output.append(line)
        #Here, handling of each line of output in real-time if needed
        print (line,end="")

    process.stdout.close()
    process.wait()
    return "".join(output)