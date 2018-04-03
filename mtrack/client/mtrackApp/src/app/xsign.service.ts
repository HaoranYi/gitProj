import { Injectable } from '@angular/core';
import { Observable } from 'rxjs/Observable';
import { of } from 'rxjs/observable/of';
import { environment } from '../environments/environment';
import { HttpClient, HttpHeaders, HttpParams } from '@angular/common/http';
import {BlockData } from './block-data';
import {SignResult, VerifyResult} from './server-response'
import {Hold, Pending, Transaction, ActionResult} from './server-response'

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


  get_vendor_id(vendor:string): Observable<number> {
    const data = { 'name': vendor };
    return this.http.post<number>(environment.apiUri+'/vendorid', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  get_all_vendors(): Observable<string[]> {
    const data = { };
    return this.http.post<string[]>(environment.apiUri+'/vendors', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  get_holds(vendor:string): Observable<Hold[]> {
    const data = { 'name': vendor };
    return this.http.post<Hold[]>(environment.apiUri+'/holds', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  get_pendings(vendor:string): Observable<Pending[]> {
    const data = { 'name': vendor };
    return this.http.post<Pending[]>(environment.apiUri+'/pendings', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  get_transactions(id:number): Observable<Transaction[]> {
    const data = { 'medicine_id': id};
    return this.http.post<Transaction[]>(environment.apiUri+'/transhistory', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  add_transactions(hold_id:number, buyer_id:number): Observable<ActionResult> {
    const data = { 'hold_id': hold_id, 'buyer_id': buyer_id };
    return this.http.post<ActionResult>(environment.apiUri+'/addtrans', JSON.stringify(data),  { headers: httpOptions.headers });
  }

  confirm_transactions(hold_id:number): Observable<ActionResult> {
    const data = { 'hold_id': hold_id };
    return this.http.post<ActionResult>(environment.apiUri+'/confirmtrans', JSON.stringify(data),  { headers: httpOptions.headers });
  }
}
