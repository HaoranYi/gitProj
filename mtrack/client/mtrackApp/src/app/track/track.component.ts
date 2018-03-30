import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';
import { VendorService } from '../vendor.service';

@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.css']
})
export class TrackComponent implements OnInit {
  title = "My Medicine";
  //@Input() vendor: string;
  public vendor: string;

  public medicines: any[];
  public transactions: any[];
  public pendings: any[];

  public trans_column_names = ["Name", "Seller", "Buyer", "Date", "State"];
  public trans_columns = ["name", "seller", "buyer", "date"];

  constructor(private router: Router, private vendorSvc: VendorService) {
    this.medicines = [
      { name: "MedA", pending: false },
      { name: "MedB", pending: true },
    ];

    this.transactions = [
      { name: "MedA", seller: "VendorB", buyer: "VendorC", date: '2018-01-02', pending: true},
      { name: "MedA", seller: "VendorA", buyer: "VendorB", date: '2018-01-01', pending: false },
    ];

    this.pendings = [
      { name: "MedC" , confirmed: false},
      { name: "MedD" , confirmed: false},
    ];

  }

  sell(name:string):void {
    console.log('sell ' + name);
    this.router.navigate(['/sell',  { id: 1, name: name } ]);
  }

  track(name:string):void {
    console.log('track ' + name);

  }

  do_confirm(name:string):void {
    console.log('do_confirm ' + name);
  }

  ngOnInit() {
    this.vendorSvc.currentVendor.subscribe(vendor=> this.vendor= vendor);
  }

}
