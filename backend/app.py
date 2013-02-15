from flask import Flask

app = None

def initialize_app(settings):
    global app
    app = Flask(__name__)
    app.config.from_object(settings)

    # ORDER MIGHT BE IMPORTANT BELOW THIS LINE
    # install extensions and import modules that do registrations
    import views ; views

    return app
