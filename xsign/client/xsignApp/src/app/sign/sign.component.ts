import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-sign',
  templateUrl: './sign.component.html',
  styleUrls: ['./sign.component.css']
})
export class SignComponent implements OnInit {
  coin: any;
  angForm: FormGroup;
  title = "Sign Product";
  result: string = "";

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
   }

  createForm() {
    this.angForm = this.fb.group({
      vendor: ['', Validators.required ],
      name: ['', Validators.required ],
      price: ['', Validators.required ]
   });
  }

  sign(vendor, name, price) {
    //this.route.params.subscribe(params => {
    //this.service.updateCoin(name, price, params['id']);
    //this.router.navigate(['index']);
    //});
    //this.result = vendor + "-" + name + "-" + price;
    this.xsignService.sign(vendor, name, price)
      .subscribe(result => this.result= result);
  }

  ngOnInit() {
    //this.route.params.subscribe(params => {
    //  this.coin = this.service.editCoin(params['id']).subscribe(res => {
    //    this.coin = res;
    //  });
    //});
  }
}

