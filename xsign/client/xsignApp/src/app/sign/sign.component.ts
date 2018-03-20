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
  title = "Sign Product";
  angForm: FormGroup;
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
   }

  createForm() {
    this.angForm = this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ]
   });
  }

  sign(vendor, produce, quantity, date) {
    this.xsignService.sign(vendor, produce, quantity, date)
      .subscribe(result => this.result = JSON.parse(result));
  }

  ngOnInit() {
    //this.route.params.subscribe(params => {
    //  this.coin = this.service.editCoin(params['id']).subscribe(res => {
    //    this.coin = res;
    //  });
    //});
  }
}

