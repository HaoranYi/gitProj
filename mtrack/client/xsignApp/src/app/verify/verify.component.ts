import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';



@Component({
  selector: 'app-verify',
  templateUrl: './verify.component.html',
  styleUrls: ['./verify.component.css']
})
export class VerifyComponent implements OnInit {
  title = "Verify product"
  angForm: FormGroup;
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
  }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ],
      signature: ['', Validators.required ]
   });
  }

  verify(vendor, produce, quantity, date, signature) {
    this.xsignService.verify(vendor, produce, quantity, date, signature)
    .subscribe(result => this.result = result);
  }

  ngOnInit() {
  }

}
