"""
Ninja Django API to collect the
"""
from ninja import Router
import subprocess
router = Router()

#TODO: update to add the argument for model_path
from django.http import StreamingHttpResponse

@router.get("/prompt_c")
def StoryTelling(request,input:str):
    assert (isinstance(input,str))
    llama2_bin = "/Users/ousheshharadhun/Documents/Workspace/FacebookLLAMA/llm_backend_go/Backend/manager/llama2.c/./run"
    llama2_model = "/Users/ousheshharadhun/Documents/Workspace/FacebookLLAMA/llm_backend_go/Backend/manager/llama2.c/stories15M.bin"

    cmd = [llama2_bin, llama2_model, "-t", "0.8", "-n", "256", "-i", input]
    process = subprocess.Popen(cmd,stdout=subprocess.PIPE,text=True)

    def stream():
        for line in iter(process.stdout.readline, ""):
            yield f"data: {line}\n\n"
            #print (f"data: {line}\n\n")
        process.stdout.close()
        process.wait()
    return StreamingHttpResponse(stream(), content_type="text/event-stream")