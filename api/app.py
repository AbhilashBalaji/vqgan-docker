import json
import os
import subprocess
from flask import Flask , request
from numpy import imag

app = Flask(__name__)
@app.route('/hello')
def hello():
    return 'Hello, World!'


# POST CALL -> runs generate.py , take optional image as input.
#  decide between sending file vs sending URI
# POST input text and image. 

@app.route('/generate',methods=['POST'])
def gen():
    data = json.loads(request.data)
    if 'input_text' in data.keys():
        # return data['input_text']
        input_text = data['input_text']
        if 'image' in data.keys():
            image = data['image']
        else :
            image = None
    else : 
        return "bruh"
    # /Users/abhilash.balaji/Desktop/image-text/vqgan-docker/api
    out = editConfig(input_text,image)
    ret = runGenScript()
    return "GEN DID NOT BREAK!!: "+str(ret) 


def editConfig(input_text:str,image=None):
    filename = '../configs/docker.json'
    with open(filename, 'r') as f:
        data = json.load(f)
        data['prompts'] = list(input_text.split(".")) # <--- add `id` value.
        if image is not None:
            if image == "forest":
                data['init_image'] = "/samples/forest.png"
            else :
                data['init_image'] = ""
    os.remove(filename)
    with open(filename, 'w') as f:
        json.dump(data, f, indent=4)
    return os.getcwd()


def runGenScript():
    # cmd = ["docker-compose", '--arg', 'value']
    cmd = list("docker-compose -f ../docker-compose.yml run generate".split())
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    for line in p.stdout:
        print(line)
    p.wait()
    return p.returncode


