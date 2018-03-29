import { Component, OnInit, Input } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-track',
  templateUrl: './track.component.html',
  styleUrls: ['./track.component.css']
})
export class TrackComponent implements OnInit {
  title = "My Medicine";
  @Input() vendor: string;

  public medicines: any[];
  public transactions: any[];
  public pendings: any[];

  public trans_column_names = ["Name", "Seller", "Buyer", "State"];
  public trans_columns = ["name", "seller", "buyer"];

  constructor() {
    this.medicines = [
      { name: "MedA", pending: false },
      { name: "MedB", pending: true },
    ];

    this.transactions = [
      { name: "MedA", seller: "VendorA", buyer: "VendorB", pending: false },
      { name: "MedA", seller: "VendorB", buyer: "VendorC", pending: true},
    ];

    this.pendings = [
      { name: "MedC" , confirmed: false},
      { name: "MedD" , confirmed: false},
    ];

  }

  sell(name:string):void {
    console.log('sell ' + name);
  }

  track(name:string):void {
    console.log('track ' + name);
  }

  do_confirm(name:string):void {
    console.log('do_confirm ' + name);
  }

  ngOnInit() {
  }

}
