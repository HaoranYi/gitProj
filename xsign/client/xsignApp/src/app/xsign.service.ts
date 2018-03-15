import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';

@Injectable()
export class XsignService {

  constructor() { }

  sign(vendor:string, name:string, price:number): Observable<string> {
    return of(vendor + '-' + name + '-' + price);
  }

}
