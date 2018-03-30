import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';

@Injectable()
export class VendorService {

  private vendorSource = new BehaviorSubject<string>("Vendor_A");
  public currentVendor = this.vendorSource.asObservable();

  constructor() { }

  changeVendor(vendor: string) {
    this.vendorSource.next(vendor)
  }
}
