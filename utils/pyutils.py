import inspect
import code

def interact(locals=None, plain=False):
    locals = locals or inspect.currentframe().f_back.f_locals
    try:
        if plain:
            raise ImportError
        from IPython import embed
        embed(user_ns=locals, banner1='')
    except ImportError:
        code.interact(local=locals)

