window.jj ?= {}

window.jj.AppView = class AppView extends Backbone.View
    template: _.template jj.jst["todo/jst/app.jst"]
    statsTemplate: _.template jj.jst["todo/jst/stats.jst"]
    events:
        'keypress #new-todo': 'createOnEnter'
        'click #clear-completed': 'clearCompleted'
        'click #toggle-all': 'toggleAllComplete'
    initialize: ->
        @buildElement()
        @allCheckbox = @$('#toggle-all')[0]
        @$input = @$('#new-todo')
        @$footer = @$('#footer')
        @$main = @$('#main')

        @listenTo @collection, 'add', @addOne
        @listenTo @collection, 'reset', @addAll
        @listenTo @collection, 'change:completed', @filterOne
        @listenTo @collection, 'all', @render

        @initRouter()

        @collection.fetch()

    initRouter : ->
        @router = new jj.Router()
        @listenTo @router, 'route:filterSet', @updateFilter

    buildElement: ->
        @.$el.html @template()
    render: ->
        completed = @collection.completed().length
        remaining = @collection.remaining().length
        if @collection.length
            @$main.show()
            @$footer.show()
            @$footer.html @statsTemplate({
                completed: completed
                remaining: remaining
            })
            @$('#filters li a').removeClass('selected').filter('[href="#/' + ( jj.app?.TodoFilter or '' ) + '"]').addClass('selected')
        else
            @$main.hide()
            @$footer.hide()
        @allCheckbox.checked = !remaining

    updateFilter : (param) ->
        jj.app.TodoFilter = param.trim() or ''
        @filterAll()

    addOne: (todo) ->
        view = new jj.TodoView({ model: todo })
        $('#todo-list').append view.render().el

    addAll: ->
        @$('#todo-list').html('')
        @collection.each(@addOne, @)

    filterOne: (todo) ->
        todo.trigger 'visible'

    filterAll: ->
        @collection.each @filterOne, @

    newAttributes: ->
        return {
            title: @.$input.val().trim()
            order: @collection.nextOrder()
            completed: false
        }

    createOnEnter: (e) ->
        if (e.which isnt jj.ENTER_KEY) or (!@.$input.val().trim() )
            return
        @collection.create @newAttributes()
        @.$input.val('')

    clearCompleted: ->
        _.invoke @collection.completed(), 'destroy'
        return false

    toggleAllComplete: ->
        completed = @allCheckbox.checked
        @collection.each (todo) ->
            todo.save {	'completed': completed }
