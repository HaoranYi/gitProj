import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";
import { VendorService } from '../vendor.service';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-sell',
  templateUrl: './sell.component.html',
  styleUrls: ['./sell.component.css']
})
export class SellComponent implements OnInit, OnDestroy {
  title: string = "Sell";
  vendor: string;
  id: number;
  name: string;
  buyer: string;
  private sub: any;
  public vendors = ["Vendor_A", "Vendor_B", "Vendor_C"];


  angForm: FormGroup;

  constructor(private route: ActivatedRoute, private vendorSvc: VendorService,
    private fb: FormBuilder, private xsignService: XsignService, private router: Router) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id'];
      this.name = params['name'];
    });
    this.vendorSvc.currentVendor.subscribe(vendor=> this.vendor= vendor);
    this.createForm();
  }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      buyer: ['', Validators.required ],
      date: ['', Validators.required ]
   });
  }


  ngOnDestroy() {
    this.sub.unsubscribe();
  }

  sell(buyer:string, date:string):void{
    console.log(this.vendor);
    console.log(this.name);
    console.log(buyer);
    console.log(date);
    this.router.navigate(['/']);
  }

  cancel():void {
    this.router.navigate(['/']);
  }
}
