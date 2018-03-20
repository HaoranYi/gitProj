import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class XsignService {

  constructor(private http: HttpClient) { }

  sign(vendor:string, produce:string, quantity:number, date:string): Observable<string> {
    const data = {
        'vendor': vendor,
        'produce': produce,
        'quantity': quantity,
        'date': date
    };

    return this.http.post(environment.apiUri+'/sign', JSON.stringify(data),  { headers: httpOptions.headers, responseType: 'text'});
  }
}
