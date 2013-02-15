console.log "core cofee loaded"
$ ->
    template = _.template jj.jst['index/hello_world.jst']
    $('body').append template()
