import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from "@angular/router";
import { VendorService } from '../vendor.service';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';


@Component({
  selector: 'app-confirm',
  templateUrl: './confirm.component.html',
  styleUrls: ['./confirm.component.css']
})
export class ConfirmComponent implements OnInit {
  title: string = "Confirm";
  name: string;
  seller: string;
  buyer: string;
  date: string;
  id: number;
  encr_data: string;
  private sub: any;

  angForm: FormGroup;

  constructor(private route: ActivatedRoute, private vendorSvc: VendorService,
    private fb: FormBuilder, private xsignService: XsignService, private router: Router) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id'];
      this.name = params['name'];
      this.date = params['date'];
      this.seller= params['seller'];
      this.encr_data = params['data'];
    });
    this.vendorSvc.currentVendor.subscribe(vendor=> this.buyer= vendor);
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

  confirm():void{
    console.log(this.name);
    console.log(this.seller);
    console.log(this.buyer);
    this.xsignService.confirm_transactions(this.id, this.encr_data).subscribe(result => {
      console.log(result);
      this.router.navigate(['/']);
    });
  }

  cancel():void {
    this.router.navigate(['/']);
  }

}
