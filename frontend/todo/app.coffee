window.jj ?= {}
window.jj.ENTER_KEY = 13

$ ->
    jj.app = new jj.AppView
        el : $('#todoapp')
        collection : new jj.TodoCollection

	Backbone.history.start()
