# http://stackoverflow.com/questions/59895/can-a-bash-script-tell-what-directory-its-stored-in
root="$( cd "$( dirname "$0" )" && pwd )"

export DEBUG=1

[ -f "${root}"/runcommands.local.sh ] && source runcommands.local.sh

unset root
