import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-medicine',
  templateUrl: './medicine.component.html',
  styleUrls: ['./medicine.component.css']
})
export class MedicineComponent implements OnInit {

  title = "Add Medicine";
  angForm: FormGroup;
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
   }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      name: ['', Validators.required ],
      qty: ['', Validators.required ],
      sn: ['', Validators.required ],
   });
  }

  add(name, qty, sn) {
    console.log(name, qty, sn); // The args are passed by temp form elt ref
    console.log(this.angForm.value); // The args are passed as json obj
  }

  ngOnInit() {
  }

}

