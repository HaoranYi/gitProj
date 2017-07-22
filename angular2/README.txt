Angular2 Notes

1. install angular cli globally. The cli helps to scafold your app.
    npm install -g @angular/cli

    ng new my-app    -- create app
    ng serve -open   -- serve app

module
    component
    template

template syntax
    - {{}} for interpolation
    - [] for property binding
    - () for event binding
    - # for variable declaration
    - * for structure directives

organize the view into sub-componet
    - app.component should be a simple shell to host those sub-component
    - use cli to create component

Use route to navigate between view/component
    - RouterModule
    - derictive {RouterOutlet, RouterLink, RouterLinkActive}
    - config: {Routes}
Use http to talk to server to get data
