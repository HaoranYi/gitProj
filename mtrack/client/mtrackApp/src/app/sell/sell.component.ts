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
  date: string;
  private sub: any;
  public vendors:string[];


  angForm: FormGroup;

  constructor(private route: ActivatedRoute, private vendorSvc: VendorService,
    private fb: FormBuilder, private xsignService: XsignService, private router: Router) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id']; // hold_id
      this.name = params['name'];
      this.date = params['date'];
    });
    this.vendorSvc.currentVendor.subscribe(vendor=> this.vendor= vendor);
    this.xsignService.get_all_vendors().subscribe(result => this.vendors=result);
    this.createForm();
  }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      buyer: ['', Validators.required ],
      date: [this.date, Validators.required ]
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

    this.xsignService.get_vendor_id(buyer).subscribe(buyer_id => {
      console.log(this.id);
      console.log(buyer_id);
      this.xsignService.add_transactions(this.id, buyer_id).subscribe(result => {
        console.log(result);
        this.router.navigate(['/']);
      });
    });

  }

  cancel():void {
    this.router.navigate(['/']);
  }
}
