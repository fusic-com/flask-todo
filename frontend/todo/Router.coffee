window.jj ?= {}

window.jj.Router = class Router extends Backbone.Router
    routes:
        '*filter': 'filterSet'
