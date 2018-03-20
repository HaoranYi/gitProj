import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
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
  blockdata: BlockData[] = [];

  result: any;

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
    this.blockdata.push(new BlockData());
  }

  deleteForm(form:FormGroup):void {
    const index: number = this.angForms.indexOf(form);
    if (index !== -1) {
      this.angForms.splice(index, 1);
      this.blockdata.splice(index, 1);
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

  verify() {
    console.log(this.blockdata.vendor);
    //this.xsignService.verify(vendor, produce, quantity, date, signature)
    //   .subscribe(result => this.result = JSON.parse(result));
  }

  ngOnInit() {
  }

}
