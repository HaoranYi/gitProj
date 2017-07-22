import { Injectable } from '@angular/core';

import { Hero } from './hero';
import { HEROES } from './mock-heroes';


// sync
// @Injectable()
// export class HeroService {
//   getHeroes(): Hero[] {
//     return HEROES;
//   }
// }

// async: return a promise
@Injectable()
export class HeroService {
    getHeroes(): Promise<Hero[]> {
        return Promise.resolve(HEROES);
    }

    getHero(id: number): Promise<Hero> {
        return this.getHeroes()
        .then(heroes => heroes.find(hero => hero.id === id));
    }
}

