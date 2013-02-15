# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
root="$( cd "$( dirname "$0" )" && pwd )"

# configuration
export DEBUG=1
export SERVER_NAME='localhost:5000'

# local runcommands
[ -f "${root}"/runcommands.local.sh ] && source runcommands.local.sh

# provision directories for dev environment
export VAR_DIR="${root}/.venv/var"
mkdir -p $VAR_DIR

unset root
