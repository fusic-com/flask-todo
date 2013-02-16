import os

class DatabaseControlError(Exception):
    pass

class UnsupportedDatabase(NotImplementedError, DatabaseControlError):
    pass

def reset_postgres_database(uri):
    if uri.hostname != 'localhost':
        for key in os.environ:
            if 'HEROKU' in key:
                print("Assuming Heroku database is blank (consider `heroku pg:reset`)")
        else:
            print("Assuming non-local database is blank")
        return
    if 0 != os.system('dropdb %(name)s && createdb %(name)s' % {'name': uri.path[1:]}):
        raise DatabaseControlError('nonzero result while recreating database (see stderr)')

def reset_database(uri):
    if uri.scheme == 'sqlite':
        if os.path.exists(uri.path):
            os.remove(uri.path)
    elif uri.scheme == 'postgres':
        reset_postgres_database(uri)
    else:
        raise UnsupportedDatabase('unknown database scheme %s' % (uri.scheme,))
