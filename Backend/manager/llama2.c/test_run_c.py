# Command to run c:
# "./run stories42M.bin -t 0.8 -n 256 -i "One day, Lily met a Shoggoth"

import subprocess


def run_binary_streamed(input_text):
    cmd = ["./run", "stories15M.bin", "-t", "0.8", "-n", "256", "-i", input_text]
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True)

    output = []
    for line in iter(process.stdout.readline, ""):
        output.append(line)
        # Here, you can handle each line of output in real-time if needed
        print(line, end="")  # This will print each line as it's being received

    process.stdout.close()
    process.wait()

    return "".join(output)


if __name__ == "__main__":
    print(run_binary_streamed("Hi Lilly"))


##Next add the rust itself to the
