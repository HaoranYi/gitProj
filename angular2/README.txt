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

* Understanding Angular route *
With angular route, the framework intercepts the http route and renders the
component directly without forwarding it the server. In traditional server
architecture, each route change is forwarded to the server and server send the
new page back.

Use http to talk to server to get data
    - HttpModule
    - mock server 
        import { InMemoryWebApiModule } from 'angular-in-memory-web-api';
        import { InMemoryDataService }  from './in-memory-data.service';
            ...
        InMemoryWebApiModule.forRoot(InMemoryDataService) // use our own 
                           //InMemoryDataService to provide data to webapi

        InMemoryDataService implements InMemoryDbService from angular-in-memory-web-api
        the url of mock server is :base/:collectionName/:id?

// for requests to an `api` base URL that gets heroes from a 'heroes' collection 
GET api/heroes          // all heroes
GET api/heroes/42       // the character with id=42
GET api/heroes?name=^j  // 'j' is a regex; returns heroes whose name starting with 'j' or 'J'
GET api/heroes.json/42  // ignores the ".json"

* typescript *
    - use `tsc` to comile *.ts to *.js
    - C# like OOP 
    - structral type
    - namespace
    - module
