window.jj ?= {}

window.jj.TodoCollection = class TodoCollection extends Backbone.Collection
    model: jj.TodoModel
    url : "/api/todos/"
    completed: ->
        return @filter((todo) ->
            return todo.get('completed')
        )
    remaining: ->
        return @without.apply @, @completed()
    nextOrder: ->
        if not @length
            return 1
        return @last().get('order') + 1
    comparator: (todo) ->
        return todo.get('order')
