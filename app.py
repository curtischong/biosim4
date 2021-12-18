from flask import Flask, request
from datetime import datetime
import re
import subprocess

app = Flask(__name__)
if __name__ == "__main__":
    app.run(host='0.0.0.0')

@app.route("/")
def hello_world():
    return """You should know what to do. The Online Judge will evaluate your solution 
with the default config. If you have changed the config, let Curtis know and he'll update the config to your new params.
You need 66.7% to get the flag. Submit to the endpoint /submit (it can take up to 30 seconds, be patient). Best of luck :)"""

@app.route("/submit")
def submit():
    genome = request.args.get("genome")
    print("submitting genome:", genome)
    if not genome or len(genome) == 0:
        return "no genome specified. retry with: /submit?genome=<genome>"
    genome = genome.replace(" ", "")
    genome = genome.replace("\n", "")
    if len(genome) % 8 != 0:
        return "genome length must be divisible by 8"

    # write the genome to the config file
    f = open("biosim4.ini", "r")
    contents = f.read().strip()
    f.close()
    loc = contents.find("startingGenome")
    contents = contents[:loc]
    contents += "startingGenome =" + genome
    f = open("biosim4.ini", "w")
    f.write(contents)
    f.close()

    # run the simulation with the specified genome
    # note: all creatures in the simulation will have the same specified genome
    result = subprocess.run(["./bin/Release/biosim4"], stdout=subprocess.PIPE)
    result = result.stdout.decode('utf-8')
    print(result)
    res = re.search("(\d*) survivors", result)
    if not res:
        return "couldn't find the number of survivors. Is your genome correct?"
    num_survivors = int(res.group(1))
    if num_survivors == 0:
        return "0 survivors. Is your genome correct?"
    percentage_survived = num_survivors/3000.0
    result_prefix = datetime.now().strftime("%I:%M:%S %p") + ": "
    if (percentage_survived >= 0.667):
        f = open(".secret.txt", "r")
        secret = f.read()
        f.close()
        return result_prefix + str(percentage_survived*100) + "% survived. Congrats! the secret key is: " + secret
    else:
        return result_prefix + str(percentage_survived*100) + "% survived"
