# sandalstrap: a barebones Python project bootstrapper
# written by Yaniv Aknin, @aknin, licensed under 2 clause BSD 
# http://sandalstrap.aknin.name/

_ns() {
    if [ -n "$VIRTUAL_ENV" ]; then
        echo 'active venv found; refusing to create another'
        return 1
    fi
    [ -z "$SND_VIRTUALENV_DIR" ] && SND_VIRTUALENV_DIR='.venv'

    if ! curl -Lfs https://raw.github.com/pypa/virtualenv/1.7/virtualenv.py | python2.7 - "$SND_VIRTUALENV_DIR"; then
        echo 'failed creating virtualenv'
        return 1
    fi

    if [ -f runcommands.sh ]; then
        echo 'source $(dirname $VIRTUAL_ENV)/runcommands.sh' >> "$SND_VIRTUALENV_DIR"/bin/activate
    fi

    source "$SND_VIRTUALENV_DIR"/bin/activate

    if [ -f requirements.txt ]; then
        if ! pip install -r requirements.txt; then
            echo 'failed installing requirements'
            return 1
        fi
    fi

    if [ "$(uname)" = "Darwin" ]; then
        if grep -q readline requirements.txt; then
            pip uninstall -y readline
            easy_install $(grep readline requirements.txt)
        else
            easy_install readline
        fi
    fi
}
_ns
