# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
root="$( cd "$( dirname "$0" )" && pwd )"

# provision directories for dev environment
export VAR_DIR="${root}/.venv/var"
mkdir -p $VAR_DIR

# configuration
export DEBUG=1
export AWS_ACCESS_KEY_ID=""
export AWS_SECRET_ACCESS_KEY=""
export SERVER_NAME='localhost:5000'
export DATABASE_URL="sqlite:///${VAR_DIR}/database.sqlite"

# local runcommands
[ -f "${root}"/runcommands.local.sh ] && source runcommands.local.sh

unset root
