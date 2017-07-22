import { Component, Input, OnInit } from '@angular/core';
import { ActivatedRoute, ParamMap } from '@angular/router';
import { Location } from '@angular/common';
import { Hero } from './hero';
import { HeroService } from './hero.service';
import 'rxjs/add/operator/switchMap';

@Component({
  selector: 'hero-detail2',
  template: `
    <div *ngIf="hero">
      <h2>{{hero.name}} details!</h2>
      <div><label>id: </label>{{hero.id}}</div>
      <div>
        <label>name: </label>
        <input [(ngModel)]="hero.name" placeholder="name"/>
      </div>
    <button (click)="goBack()">Back</button>
    </div>
  `
})
export class HeroDetailComponent2 implements OnInit{
    constructor(private heroService: HeroService,
        private route: ActivatedRoute,
        private location: Location) {}

    // switchMap maps id in observable route parameter to a new observable - the
    // result of HeroService.getHero(). If the user re-navigate to this
    // component, and the old request is still pending, swithMap will cancels the
    // old request and call HeroService.getHero() again.
    // (+) operator convert id to string.
    // no need to unsubscribe, because swithMap manages observable and the
    // subscription are cleaned up when the component is destroyed.
    ngOnInit(): void {
        this.route.paramMap
        .switchMap((params: ParamMap) => this.heroService.getHero(+params.get('id')))
        .subscribe(hero => this.hero = hero);
    }


goBack(): void {
    this.location.back();
}


@Input() hero: Hero;
}

