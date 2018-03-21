import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { forkJoin } from 'rxjs/observable/forkJoin';
import { XsignService } from '../xsign.service';
import {BlockData } from '../block-data';


@Component({
  selector: 'app-chain',
  templateUrl: './chain.component.html',
  styleUrls: ['./chain.component.css']
})
export class ChainComponent implements OnInit {
  title = "Verify chain"
  angForms: FormGroup[] = [];

  results: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.addForm();
  }

  addForm():void {
    this.angForms.push(this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ],
      signature: ['', Validators.required ]
    }));
    if (this.results) {
      this.results = null;
    }
  }

  deleteForm(form:FormGroup):void {
    const index: number = this.angForms.indexOf(form);
    if (index !== -1) {
      this.angForms.splice(index, 1);
    }
    if (this.results) {
      this.results = null;
    }
  }

  isFormValid():boolean{
    for (let angForm of this.angForms) {
      if (angForm.pristine || angForm.invalid) {
        return false;
      }
    }
    return true;
  }

  verify():void {
    forkJoin(
      this.angForms.map((x)=> x.value)
      .map(x=>{return this.xsignService.verify(x.vendor, x.produce, x.quantity, x.date, x.signature) })
    ).subscribe(x => {this.results = x.map(y=>JSON.parse(y));});
  }

  ngOnInit() {
  }

}
