window.jj ?= {}

window.jj.TodoModel = class TodoModel extends Backbone.Model
    defaults:
        title: ''
        completed: false
    toggle: ->
        @save { completed: !@get('completed') }
