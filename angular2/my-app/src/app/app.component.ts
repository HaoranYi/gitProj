import { Component, OnInit } from '@angular/core';
import { Hero } from './hero';
import { HeroService } from './hero.service';

//export class Hero {
//    id: number;
//    name: string;
//}

//const HEROES: Hero[] = [
//  { id: 11, name: 'Mr. Nice' },
//  { id: 12, name: 'Narco' },
//  { id: 13, name: 'Bombasto' },
//  { id: 14, name: 'Celeritas' },
//  { id: 15, name: 'Magneta' },
//  { id: 16, name: 'RubberMan' },
//  { id: 17, name: 'Dynama' },
//  { id: 18, name: 'Dr IQ' },
//  { id: 19, name: 'Magma' },
//  { id: 20, name: 'Tornado' }
//];
 

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css'],
  providers: [HeroService] // inject service
})
export class AppComponent {
  title = 'Dongyin App';
  hero = {id:1, name: 'windstorm'};
  //heros = HEROES;
  heroes:Hero[]; 
  selectedHero:Hero = null;

  // inject HeroService on demand
  constructor(private heroService: HeroService) { }
 
  // async call to get data
  getHeroes(): void {
    this.heroService.getHeroes().then(heroes => this.heroes = heroes);
  }
 
  // getData on ngOnInit
  ngOnInit(): void {
    this.getHeroes();
  }

  clicked() {
      if (this.title == 'Dongyin App') {
          this.title = 'abc';
      } else {
          this.title = 'Dongyin App';
      }
  }


  onSelect(hero: Hero): void {
    this.selectedHero = hero;
  }
}

   
