import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import {BlockData } from './block-data';
import {SignResult, VerifyResult} from './server-response'

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable()
export class XsignService {

  constructor(private http: HttpClient) { }

  sign(vendor:string, produce:string, quantity:number, date:string): Observable<SignResult> {
    const data = {
        'vendor': vendor,
        'produce': produce,
        'quantity': quantity,
        'date': date
    };
    return this.http.post<SignResult>(environment.apiUri+'/sign', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  verify(vendor:string, produce:string, quantity:number, date:string, signature:string): Observable<VerifyResult> {
    const data = {
        'vendor': vendor,
        'produce': produce,
        'quantity': quantity,
        'date': date,
        'signature': signature
    };
    return this.http.post<VerifyResult>(environment.apiUri+'/verify', JSON.stringify(data),  { headers: httpOptions.headers });
  }
}
