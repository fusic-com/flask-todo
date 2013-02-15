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
export SECRET_KEY="development"

# local runcommands
[ -f "${root}"/runcommands.local.sh ] && source runcommands.local.sh

# functions
function cloud_setup() {
    [ -z "$1" ] && { echo "usage: $0 <setup-name>"; return 1; }
    echo "Switching this environment to use $1 resources"
    set -a
    source <(heroku config -s -a $1 < /dev/null)
    set +a
    if [ "$SECRET_KEY" = "development" ]; then
        warning "Failed getting setup configuration or setup has invalid SECRET_KEY variable"
        return 1
    fi
    source <(python << EOF
import urlobject
url = urlobject.URLObject("$DATABASE_URL")
def out(k, v): print("export %s=%s" % (k,v))
out("PGHOST", url.hostname)
out("PGUSER", url.username)
out("PGPASSWORD", url.password)
out("PGDATABASE", url.path[1:])
EOF
)
}

unset root
