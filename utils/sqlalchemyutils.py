from sqlalchemy.sql.expression import ClauseElement
from sqlalchemy.orm.exc import NoResultFound

def get_or_create(db, model, defaults=None, **kwargs):
    """a fairly simple (read: simplistic, dangerous, poor-performance) version of an upsert function.
       see: http://www.depesz.com/2012/06/10/why-is-upsert-so-complicated/
       and: http://www.postgresql.org/docs/current/static/plpgsql-control-structures.html#PLPGSQL-UPSERT-EXAMPLE
       for inspiration on how to improve it.
       in particular:
        - this version is raced between the filter_by() and the insert (might raise an exception)
        - if you want "get and update or create" semantics, and your backend supports RETURNING, you will do fewer
           db roundtrips by using UPDATE ... RETURNING and INSERT ... RETURNING; which can't be done with this version
    """
    try:
        return model.query.filter_by(**kwargs).one(), False
    except NoResultFound:
        pass
    params = {k: v for k, v in kwargs.iteritems()
              if not isinstance(v, ClauseElement)}
    params.update(defaults or {})
    instance = model(**params)
    db.make_transient(instance)
    db.session.add(instance)
    return instance, True
