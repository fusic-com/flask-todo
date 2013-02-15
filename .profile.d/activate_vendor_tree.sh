#!sh

export PATH="/app/vendor/bin:$PATH"
export CFLAGS="-I/app/vendor/include"
export LDFLAGS="-L/app/vendor/lib -R/app/vendor/lib"
export LD_LIBRARY_PATH="/app/vendor/lib:$LD_LIBRARY_PATH"

python_path_segment="/app/vendor/lib/python2.7/dist-packages:/app/vendor/lib/python2.7/dist-packages"
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$python_path_segment"
else
    export PYTHONPATH="$python_path_segment:$PYTHONPATH"
fi
unset python_path_segment
