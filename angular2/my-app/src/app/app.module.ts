import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { FormsModule }   from '@angular/forms';
import { RouterModule } from '@angular/router'; // for routes

import { AppComponent } from './app.component';
import { HeroesComponent } from './heroes.component';
import { HeroDetailComponent } from  './hero-detail.component';
import { HeroDetailComponent2 } from './hero-detail.component2';
import { DashboardComponent } from './dashboard.component';
import { HeroService } from './hero.service';



@NgModule({
  declarations: [
    AppComponent,
      HeroDetailComponent,
      HeroDetailComponent2,
      HeroesComponent,
      DashboardComponent
  ],
  imports: [
      BrowserModule,
      FormsModule,
      RouterModule.forRoot([
        {
              path:'',
              redirectTo:'/dashboard',
              pathMatch:'full'
          },
          {
            path:'heroes',
            component:HeroesComponent
          },
          {
              path:'dashboard',
              component:DashboardComponent
          },
          {
              path:'detail/:id',
              component: HeroDetailComponent2
          },
          {
              path:'about',
              component: HeroesComponent
          }
        ])
  ],
  providers: [HeroService],
  bootstrap: [AppComponent]
})
export class AppModule { }
