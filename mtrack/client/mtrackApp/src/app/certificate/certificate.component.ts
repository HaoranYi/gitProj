import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-certificate',
  templateUrl: './certificate.component.html',
  styleUrls: ['./certificate.component.css']
})
export class CertificateComponent implements OnInit {

  title = "Add Certificate";
  angForm: FormGroup;
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
   }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      company: ['', Validators.required ],
      pubkey: ['', Validators.required ],
   });
  }

  add(company, pubkey) {
    console.log(company, pubkey); // The args are passed by temp form elt ref
    console.log(this.angForm.value); // The args are passed as json obj
  }

  ngOnInit() {
  }

}
