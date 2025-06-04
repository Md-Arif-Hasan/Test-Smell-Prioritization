#!/bin/bash

# File: unique_contributors.sh

REPOS=(
"https://github.com/18F/domain-scan.git"
"https://github.com/21dotco/two1-python.git"
"https://github.com/Epistimio/orion.git"
"https://github.com/Ericsson/codechecker.git"
"https://github.com/EricssonResearch/calvin-base.git"
"https://github.com/Exa-Networks/exabgp.git"
"https://github.com/F5Networks/f5-common-python.git"
"https://github.com/FAForever/client.git"
"https://github.com/Fizzadar/pyinfra.git"
"https://github.com/LinOTP/LinOTP.git"
"https://github.com/ROCmSoftwarePlatform/Tensile.git"
"https://github.com/RaRe-Technologies/gensim.git"
"https://github.com/RasaHQ/rasa-sdk.git"
"https://github.com/Yubico/yubikey-manager.git"
"https://github.com/YunoHost/yunohost.git"
"https://github.com/Zulko/moviepy.git"
"https://github.com/aajanki/yle-dl.git"
"https://github.com/aiidateam/aiida-core.git"
"https://github.com/aio-libs/aiohttp.git"
"https://github.com/aio-libs/aiokafka.git"
"https://github.com/aio-libs/aiomysql.git"
"https://github.com/aio-libs/aioredis.git"
"https://github.com/aiortc/aiortc.git"
"https://github.com/airspeed-velocity/asv.git"
"https://github.com/aldebaran/qibuild.git"
"https://github.com/arrow-py/arrow.git"
"https://github.com/arsenetar/dupeguru.git"
"https://github.com/asciidoc/asciidoc-py3.git"
"https://github.com/asdf-format/asdf.git"
"https://github.com/astropy/astroplan.git"
"https://github.com/automl/SMAC3.git"
"https://github.com/automl/auto-sklearn.git"
"https://github.com/avocado-framework/avocado.git"
"https://github.com/awesto/django-shop.git"
"https://github.com/aws-quickstart/taskcat.git"
"https://github.com/aws/aws-cli.git"
"https://github.com/aws/aws-elastic-beanstalk-cli.git"
"https://github.com/aws/aws-sam-cli.git"
"https://github.com/aws/chalice.git"
"https://github.com/awslabs/aws-data-wrangler.git"
"https://github.com/azavea/raster-vision.git"
"https://github.com/bcb/jsonrpcserver.git"
"https://github.com/bear/python-twitter.git"
"https://github.com/beeware/briefcase.git"
"https://github.com/beeware/toga.git"
"https://github.com/beeware/voc.git"
"https://github.com/behave/behave.git"
"https://github.com/bethgelab/foolbox.git"
"https://github.com/pydoit/doit.git"
"https://github.com/thouska/spotpy.git"
"https://github.com/whoosh-community/whoosh.git"
"https://github.com/dbcli/mycli.git"
)

# Output files
CLONE_DIR="cloned_repos"
TMP_FILE="all_contributors_raw.csv"
FINAL_FILE="unique_contributors.csv"

mkdir -p "$CLONE_DIR"
> "$TMP_FILE"

cd "$CLONE_DIR" || exit

for REPO in "${REPOS[@]}"; do
    REPO_NAME=$(basename "$REPO" .git)
    if [ ! -d "$REPO_NAME" ]; then
        echo "Cloning $REPO_NAME..."
        git clone --quiet "$REPO"
    fi
    cd "$REPO_NAME" || continue
    echo "Extracting from $REPO_NAME..."
    git log --format='%an,%ae' >> "../../$TMP_FILE"
    cd ..
done

cd ..

# Remove duplicates and save final unique list
sort "$TMP_FILE" | uniq > "$FINAL_FILE"

echo "✅ Unique contributors saved to $FINAL_FILE"
