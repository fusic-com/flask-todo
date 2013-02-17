window.jj ?= {}

window.jj.TodoView = class TodoView extends Backbone.View
    tagName:  'li'
    template: _.template jj.jst["todo/jst/item.jst"]
    events:
        'click .toggle':	'toggleCompleted'
        'dblclick label':	'edit'
        'click .destroy':	'clear'
        'keypress .edit':	'updateOnEnter'
        'blur .edit':		'close'
    initialize: ->
        @listenTo @model, 'change', @render
        @listenTo @model, 'destroy', @remove
        @listenTo @model, 'visible', @toggleVisible

    render: ->
        @$el.html @template(@model.toJSON())
        @$el.toggleClass 'completed', @model.get('completed')
        @toggleVisible()
        @$input = @$('.edit')
        return @

    toggleVisible: ->
        @.$el.toggleClass 'hidden',  @isHidden()

    isHidden: ->
        isCompleted = @model.get('completed')
        return (!isCompleted and (jj.app?.TodoFilter is 'completed')) or (isCompleted and (jj.app?.TodoFilter is 'active'))

    toggleCompleted: ->
        @model.toggle()

    edit: ->
        @$el.addClass 'editing'
        @$input.focus()

    close: ->
        value = @$input.val().trim()
        if value
            @model.save { title: value }
        else
            @clear()
        @$el.removeClass 'editing'
    updateOnEnter: (e) ->
        if e.which is jj.ENTER_KEY
            @close()

    clear: ->
        @model.destroy()
