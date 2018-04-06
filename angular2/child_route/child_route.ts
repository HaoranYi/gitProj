// route map
export const routes: Routes = [
  { path: '', redirectTo: 'product-list', pathMatch: 'full' },
  { path: 'product-list', component: ProductList },
  { path: 'product-details/:id', component: ProductDetails,
    children: [
      {path: '', redirectTo: 'overview', pathMatch: 'full' },
      {path: 'overview', component: Overview },
      {path: 'specs', component: Specs },
    ]
  }
];

// route-outlet
import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivateRoute } from '@angular/router';

@component({
  selector: 'product-details',
  tempalte `
  <p>Product Details: {{id}}</p>
  <!-- Product information -->
  <nav>
    <a [routerLink]="['overview']">Overview</a>
    <a [routerLink]="['specs']">Technical Specs</a>
  </nav>
  <router-outlet></router-outlet>
  <!-- Overview & Specs components get added here by the router -->
  `
})

export default class ProductDetails implements OnInit, OnDestroy {
  id: number;

  constructor(private route: ActivatedRoute) {}

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id'];
    });
  }

  ngOnDestroy() {
    this.sub.unsubscripte();
  }
}

// accessing parent's route's parameter
export default class Overview {
  parentRouteId: number;
  private sub: any;

  constructor(private router: Router,
    private route: ActivatedRoute) {}

  ngOnInit() {
    // Get parent ActivatedRoute of this route.
    this.sub = this.router.routerState.parent(this.route)
      .params.subscribe(params => {
        this.parentRouteId = +params["id"];
      });
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}

// links
//  prefix     looks in
//  /          root of the app
//  none       current component child routes
//  ../        current component parent routes
<a [routerLink]="['route-one']">Route One</a>
<a [routerLink]="['../route-two']">Route Two</a>
<a [routerLink]="['/route-three']">Route Three</a>
