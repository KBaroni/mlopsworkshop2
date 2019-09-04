"""
Copyright (C) Microsoft Corporation. All rights reserved.​
 ​
Microsoft Corporation (“Microsoft”) grants you a nonexclusive, perpetual,
royalty-free right to use, copy, and modify the software code provided by us
("Software Code"). You may not sublicense the Software Code or any use of it
(except to your affiliates and to vendors to perform work on your behalf)
through distribution, network access, service agreement, lease, rental, or
otherwise. This license does not purport to express any claim of ownership over
data you may have shared with Microsoft in the creation of the Software Code.
Unless applicable law gives you more rights, Microsoft reserves all other
rights not expressly granted herein, whether by implication, estoppel or
otherwise. ​
 ​
THE SOFTWARE CODE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
MICROSOFT OR ITS LICENSORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO,
PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR
BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER
IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
ARISING IN ANY WAY OUT OF THE USE OF THE SOFTWARE CODE, EVEN IF ADVISED OF THE
POSSIBILITY OF SUCH DAMAGE.
"""
import os
import json
import sys
from azureml.core import Run
from azureml.core.model import Model
import argparse

from azureml.core.authentication import AzureCliAuthentication

cli_auth = AzureCliAuthentication()

# Get workspace
# ws = Workspace.from_config(auth=cli_auth, path='./')


run = Run.get_context()
exp = run.experiment
ws = run.experiment.workspace

parser = argparse.ArgumentParser("register")
parser.add_argument(
    "--config_suffix", type=str, help="Datetime suffix for json config files"
)
parser.add_argument(
    "--json_config",
    type=str,
    help="Directory to write all the intermediate json configs",
)
parser.add_argument(
    "--model_name",
    type=str,
    help="Name of the Model",
    default="sklearn_regression_model.pkl",
)

args = parser.parse_args()

print("Argument 1: %s" % args.config_suffix)
print("Argument 2: %s" % args.json_config)

if not (args.json_config is None):
    os.makedirs(args.json_config, exist_ok=True)
    print("%s created" % args.json_config)

evaluate_run_id_json = "run_id_{}.json".format(args.config_suffix)
evaluate_output_path = os.path.join(args.json_config, evaluate_run_id_json)
model_name = args.model_name

# Get the latest evaluation result
try:
    with open(evaluate_output_path) as f:
        config = json.load(f)
    if not config["run_id"]:
        raise Exception(
            "No new model to register as production model perform better")
except Exception:
    print("No new model to register as production model perform better")
    sys.exit(0)

run_id = config["run_id"]
experiment_name = config["experiment_name"]
# exp = Experiment(workspace=ws, name=experiment_name)

run = Run(experiment=exp, run_id=run_id)
names = run.get_file_names
names()
print("Run ID for last run: {}".format(run_id))
model_local_dir = "model"
os.makedirs(model_local_dir, exist_ok=True)

# Download Model to Project root directory
# model_name = "sklearn_regression_model.pkl"
run.download_file(
    name="./outputs/" + model_name, output_file_path="./model/" + model_name
)
print("Downloaded model {} to Project root directory".format(model_name))
os.chdir("./model")
model = Model.register(
    model_path=model_name,  # this points to a local file
    model_name=model_name,  # this is the name the model is registered as
    tags={"area": "diabetes", "type": "regression", "run_id": run_id},
    description="Regression model for diabetes dataset",
    workspace=ws,
)
os.chdir("..")
print(
    "Model registered: {} \nModel Description: {} \nModel Version: {}".format(
        model.name, model.description, model.version
    )
)

# Remove the evaluate.json as we no longer need it
# os.remove("aml_config/evaluate.json")

# Writing the registered model details to /aml_config/model.json
model_json = {}
model_json["model_name"] = model.name
model_json["model_version"] = model.version
model_json["run_id"] = run_id
filename = "model_{}.json".format(args.config_suffix)
output_path = os.path.join(args.json_config, filename)
with open(output_path, "w") as outfile:
    json.dump(model_json, outfile)
