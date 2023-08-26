from django.http import StreamingHttpResponse
import subprocess
from ninja import Router

router = Router()


# The subprocess command
@router.get("/stream")
def generate_output(request):
    def stream_output():
        command = [
            "./build/bin/gpt-2",
            "-m",
            "models/gpt-2-117M/ggml-model-gpt-2-1558M.bin",
            "-p",
            "What is the capital of France?",
        ]

        try:
            process = subprocess.Popen(
                command,
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,
                text=True,
                bufsize=1,
                universal_newlines=True,
            )

            for line in iter(process.stdout.readline, ""):
                yield line
        except Exception as e:
            yield f"An error occurred: {e}"

    response = StreamingHttpResponse(stream_output(), content_type="text/plain")
    return response
