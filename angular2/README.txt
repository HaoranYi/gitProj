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
    - [(ngModel)] to do 2-way data binding

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

jquery like web element selection and update
    // use @ViewChild to get the html element
    @ViewChild('<myElementId>') myElement: ElementRef;
    // apply js library on the element
    Plotyly.newPlot(this.myElement, data, layout, config);


When making http call through restful api, the server have to enable cors, which
is a filter that add headers on the request:
    Access-Control-Allow-Origin,
    Access-Control-Allow-Methods,
    Access-Control-Max-Age,
    Access-Control-Allow-Headers
This can be implemented as python decroator for flask.

* Observable and Promise *
http client makes request to restful server and return Observable. Observable
is async array.

import { http } from '@angular/http'
import { Observable } from 'rxjs/Observable'
import 'rxjs/add/operator/map'

* rxjs library implements Observable. *
Core type:
    - Observable: callable future values or events
Satellite types:
    - Observer: callbacks that listen to values delivered by Observable
    - Subscription: exec of an observable
        - call .Subscribe() to execute an observable
    - Subject: eventEmitter multicast a value/event to multiple Observers
    - Scheduler: centralized dispatcher to control concurrency, i.e.
      setTimeout/requestAnimationFrame
Operators: map, filter, reduce, every etc.

Use rxjs/add/... to add more functionality to Observable.
Use |async to access Observable in html template
Use 'Subject' to create producer stream
    - .next(stuff) to push stuff into the steam
Array-like operations on Observable
    - map: apply function on the Observable
    - switchMap: discard old Observable and jump to new ones
    - deboundTime: wait certain ms after key stroke event
    - distinctUntilChanged: ignore same value
An operation is a function with creates a new Observable based on the current
Observable. This is a pure operation: the previous Observable stays
unmodified. Subscribing the output Observable will also subscribe to the input
Observable.

Observable.toPromise() will return a promise object, this is good for one time
request/response usage.

category of operations:
    - create Observable
    - transoform Observable
    - filter Observable
    - combine Observable
    - mulitcasting (with subject)
    - utility operations
    - aggregate operations
