# make sure any failed command immediately returns exit status
set -eo pipefail

# install required packages
pip install -r requirements.txt
