import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";
import { VendorService } from '../vendor.service';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';


@Component({
  selector: 'app-history',
  templateUrl: './history.component.html',
  styleUrls: ['./history.component.css']
})
export class HistoryComponent implements OnInit {

  public transactions: any[];
  public name: string;
  public vendor: string;
  public id: number;
  private sub: any;
  public trans_column_names = ["Name", "Seller", "Buyer", "Date", "State"];
  public trans_columns = ["name", "seller", "buyer", "date"];



  constructor(private route: ActivatedRoute, private vendorSvc: VendorService,
    private fb: FormBuilder, private xsignService: XsignService, private router: Router) {
      this.transactions = [
      { name: "MedA", seller: "VendorB", buyer: "VendorC", date: '2018-01-02', pending: true},
      { name: "MedA", seller: "VendorA", buyer: "VendorB", date: '2018-01-01', pending: false },
    ];


  }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id'];
      this.name = params['name'];
    });
    this.vendorSvc.currentVendor.subscribe(vendor=> this.vendor= vendor);
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  goback():void {
    this.router.navigate(['/']);
  }

}
