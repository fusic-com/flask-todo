This is a short todo backbone example app, it is based on Addy Osmani's work in the TodoMVC project.
Original project is can be found here: http://addyosmani.github.com/todomvc/

Main changes from the original:
    - re-written in coffee
    - Templates are packaged by the assets pipe-line and are place under the jj.jst namesapce
    - AppView gets an empty element and build what is need through a template, so it is less dependent on existing dom
    - AppView gets the Todo collection at init and doesn't depend on a global beeing available
