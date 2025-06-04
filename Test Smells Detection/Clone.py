import os
import subprocess
import time

# Target directory
CLONE_DIR = ".../Pynose_Projects"

# List of Python projects to clone (50 diverse projects)
projects = [
    "https://github.com/18F/domain-scan.git",
"https://github.com/21dotco/two1-python.git",
"https://github.com/Epistimio/orion.git",
"https://github.com/Ericsson/codechecker.git",
"https://github.com/EricssonResearch/calvin-base.git",
"https://github.com/EventGhost/EventGhost.git",
"https://github.com/Exa-Networks/exabgp.git",
"https://github.com/F5Networks/f5-ansible.git",
"https://github.com/F5Networks/f5-common-python.git",
"https://github.com/FAForever/client.git",
"https://github.com/FederatedAI/FATE.git",
"https://github.com/Fizzadar/pyinfra.git",
"https://github.com/Flexget/Flexget.git",
"https://github.com/LinOTP/LinOTP.git",
"https://github.com/ROCmSoftwarePlatform/Tensile.git",
"https://github.com/RaRe-Technologies/gensim.git",
"https://github.com/RasaHQ/rasa-sdk.git",
"https://github.com/Rhizome-Conifer/conifer.git",
"https://github.com/Yubico/yubikey-manager.git",
"https://github.com/YunoHost/yunohost.git",
"https://github.com/Zulko/moviepy.git",
"https://github.com/aajanki/yle-dl.git",
"https://github.com/aerospike/aerospike-client-python.git",
"https://github.com/aiidateam/aiida-core.git",
"https://github.com/aio-libs/aiohttp.git",
"https://github.com/aio-libs/aiokafka.git",
"https://github.com/aio-libs/aiomysql.git",
"https://github.com/aio-libs/aioredis.git",
"https://github.com/aiortc/aiortc.git",
"https://github.com/airspeed-velocity/asv.git",
"https://github.com/aldebaran/qibuild.git",
"https://github.com/arrow-py/arrow.git"
"https://github.com/arsenetar/dupeguru.git",
"https://github.com/asciidoc/asciidoc-py3.git"
"https://github.com/asdf-format/asdf.git"
"https://github.com/astropy/astroplan.git"
"https://github.com/authomatic/authomatic.git",
"https://github.com/automl/SMAC3.git",
"https://github.com/automl/auto-sklearn.git",
"https://github.com/autorope/donkeycar.git",
"https://github.com/avocado-framework/avocado.git",
"https://github.com/awesto/django-shop.git"
"https://github.com/aws-cloudformation/cfn-python-lint.git",
"https://github.com/aws-quickstart/taskcat.git",
"https://github.com/aws/aws-cli.git",
"https://github.com/aws/aws-elastic-beanstalk-cli.git",
"https://github.com/aws/aws-sam-cli.git",
"https://github.com/aws/chalice.git",
"https://github.com/awslabs/aws-data-wrangler.git",
"https://github.com/azavea/raster-vision.git",
"https://github.com/bcb/jsonrpcserver.git",
"https://github.com/bear/python-twitter.git",
"https://github.com/beeware/briefcase.git",
"https://github.com/beeware/toga.git",
"https://github.com/beeware/voc.git",
"https://github.com/behave/behave.git",
"https://github.com/bethgelab/foolbox.git",
"https://github.com/catalyst-team/catalyst.git",
"https://github.com/dbcli/mycli.git",
"https://github.com/gitpython-developers/GitPython.git",
"https://github.com/psd-tools/psd-tools.git",
"https://github.com/pydoit/doit.git",
"https://github.com/thouska/spotpy.git"
"https://github.com/whoosh-community/whoosh.git"
]

def clone_projects():
    # Create directory if it doesn't exist
    if not os.path.exists(CLONE_DIR):
        os.makedirs(CLONE_DIR)
        print(f"Created directory: {CLONE_DIR}")

    # Change to the target directory
    os.chdir(CLONE_DIR)
    print(f"Changed to directory: {CLONE_DIR}")

    # Clone each project
    for i, repo_url in enumerate(projects, 1):
        # Extract project name from URL
        project_name = repo_url.split('/')[-1].replace('.git', '')
        
        # Skip if project already exists
        if os.path.exists(os.path.join(CLONE_DIR, project_name)):
            print(f"[{i}/50] Skipping {project_name} - already exists")
            continue

        print(f"[{i}/50] Cloning {project_name}...")
        try:
            # Clone with depth=1 to save time and space
            subprocess.run(['git', 'clone', repo_url], 
                         check=True, 
                         stdout=subprocess.PIPE, 
                         stderr=subprocess.PIPE)
            print(f"Successfully cloned {project_name}")
            
            # Small delay to avoid overwhelming the server
            time.sleep(1)
            
        except subprocess.CalledProcessError as e:
            print(f"Error cloning {project_name}: {e}")
            continue

if __name__ == "__main__":
    print("Starting to clone 50 Python projects...")
    clone_projects()
    print("Cloning process completed!")