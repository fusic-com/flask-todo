# flask-todo

`flask-todo` is a sample app that is largely yet-another implementation of Addy Osmani's [`TodoMVC`](http://addyosmani.github.com/todomvc/) project. What seriously differentiates `flask-todo` from `TodoMVC` is that `flask-todo` has a substantial backend (server-side code) supporting the frontend features. The idea is to present one possible architecture for a modern web application, based on Flask and Backbone.js (and a lot of other libraries).

Infrastructure and layout are deeply tied to the size of the project - no use boilerplating (or implementing) a ton of infrastructure for a quick weekend project, and it's impossible to write a large scale project without infrastructure or a tidy layout. We believe `flask-todo` is correctly structured for a small team's project of several person years, more or less what you'd expect a web based startup to do on a round or two of funding.

## What's inside?

1. Directory layout for a non-trivial Flask/Python webapp
2. Our home brewed [12 factor](http://www.12factor.net/) inspired environment oriented configuration
3. Deployment/provisioning helpers for localhost development and Heroku deploys
4. `flask-script` based management commands
5. `flask-assets`/`webassets` based asset management (CoffeeScript, SCSS, minification, concatenation, JSTs)
6. `flask-sqlalchemy`/`sqlalchemy` based database persistence
7. `flask-login` based auth, with substantial additions and Backbone.js based frontend helpers
8. `flask-restful` based resource-oriented API (our API is not Roy Fieldingly RESTful, but we like it)
9. Our home brewed logging strategy for Flask, which among other things attaches a request-id to each request

## Installation

To run `flask-todo` you will need to "bootstrap" it with a very lightweight bootstrapping system we call *sandalstrap*. As a convenience, a shell script which goes through the moves of sandalstrap can be found in the file `sandalstrap` (also available [here](http://sandalstrap.aknin.name)), so you can do something like:

    $ git clone https://github.com/yaniv-aknin/flask-todo.git
        ...
    $ cd flask-todo
    $ source sandalstrap.sh
        ...
    $ ./manage.py recreatedb
    $ ./manage.py runserver
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader

Bascially, the script creates and activates a virtualenv in a directory called `.venv`, install `requirements.txt` and source `runcommands.sh`. `runcommands.sh` is a shell script that should be sourced into your environment when you activate the project's virtualenv, and it does things like setup the development configuration (in your environment) and provision (or tell you to manually provision) required platform elements like cache directories or non-pip-installable binary packages (this idea is somewhat similar to [autoenv](https://github.com/kennethreitz/autoenv)'s `.env` file). The sandalstrap script will patch your virtualenv's activation script so it will source `runcommands.sh` on startup (it doesn't patch the c-shell or Python activators; we weren't troubled by this at all).

When you first sandalstrap the project, it may tell you all sorts of stuff is missing (the `coffee` executable, for example), and you should install what it tells you to. We opted for bootstrap simplicity rather than exhaustiveness, so if installing requirements fails, you should see what's missing manually and install it yourself. At the time of this writing, you'll save yourself some trouble if you make sure you have git, a build environment, Python 2.7, libevent, a Java runtime and CoffeeScript before attempting installation (`sudo apt-get install git build-essential python2.7-dev libevent-dev openjdk-6-jre coffeescript openjdk-6-jre`).

Sandalstrapping is way simpler and lighter than buildout or vagrant, but achieves all we've needed. We hope other projects will adopt it, but your mileage may vary.

## Deployment

`flask-todo` is ready to be deployed on Heroku as-is, and should be fairly easy to deploy elsewhere, too. To deploy to Heroku, do the following:

1. Create a new Heroku Cedar app (`heroku apps:create -a flask-todo -s cedar`).
2. Review `config/settings.py` and configure all `required()` settings (`heroku config:set KEY=VALUE`...)
3. Provision any necessary add-ons; at this time, you only need a database (`heroku addons:add heroku-postgresql:dev`)
4. Promote the database to the primary database (`heroku pg:promote HEROKU_POSTGRESQL_`COLOR`_URL`)
4. Enable [slug compilation time configuraiton](https://devcenter.heroku.com/articles/labs-user-env-compile) (`heroku labs:enable user-env-compile`)
4. Push the code to Heroku (`git push heroku master:master`)
5. Create the database (`heroku run manage.py recreatedb`)

Take note of the shell function `cloud_setup()`, included in `runcommands.sh`. `cloud_setup` sources the configuration of an Heroku app into your environment, so you can run the development shell and other management commands (`psql`, etc) against the backing services of your cloud deployment. Very useful and in our opinion compatible with the 12 factor manifest.

## Postgres
We believe in 12 factor dev/prod parity and do our own development with postgres, not SQLite. However, we felt that forcing people to install postgres might be detrimental to our project's success. Hence, we opted to make the project work without postgres or `psycopg2` by default, and resort to an uglyish requirement injection hack when deploying to Heroku. If you do any kind of serious development based on flask-todo, we implore you to add `psycopg2` to your `requirements.txt` file, install Postgres locally and set your development `DATABASE_URL` in `runcommands.txt` to your postgres database. See more [here](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

## Caveats

`flask-todo` is based on the future codebase of Fusic, and was never run in production (this will change shortly). In addition to any number of unknown bugs, it has the following caveats/unreleased-features/planned-features (in no particular order):

1. Deployment of built assets to S3 with versioning *(see below)*
2. HTTP caching
3. Facebook authentication
4. Facebook Opengraph tags
5. GZip middleware
6. System resources (favicon, robots.txt, sitemap.xml...)
7. Storage abstraction (something like flask-storage)
8. Asynchronous task execution
9. Image spritalizer (something like [this](https://github.com/miracle2k/webassets/issues/124))
10. Unittests
11. Integration with more external services.

Regarding deployment of assets to S3: this could be a serious issue. Built assets are versioned, and a new deployment won't be able to serve old assets (it simply doesn't have them). On a decently busy site, code deployments might cause clients to break because old HTML tries to access old-and-unavailable resources. This isn't a show stopper, but it's serious, especially if you want to let clients cache the HTML for any reasonable period.

Even with these caveats, we believe `flask-todo` would have helped us a lot when we started, and we hope it will help you. We will try to slowly fix these caveats, but no promises. That said, if anyone would like to turn `flask-todo` into a community effort and try to contribute something from this list (or different altogether, but we suggest you discuss it with us first) - be our guest!

## Contributors

`flask-todo` was written by Yaniv Aknin (`@aknin`) and Yaniv Ben-Zaken (`@cizei`) in an attempt to provide a free and open source web application which is larger than a typical "tutorial hello world" kind of app. It is heavily based on the codebase behind [www.fusic.com](http://www.fusic.com), our gracious employer who kindly allowed us to adapt and release these non-business specific parts of our codebase. Most code here was written by us as part of our job, some of it was written by the other great folks at Fusic.

