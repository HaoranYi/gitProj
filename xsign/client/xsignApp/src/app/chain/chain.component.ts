import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';


@Component({
  selector: 'app-chain',
  templateUrl: './chain.component.html',
  styleUrls: ['./chain.component.css']
})
export class ChainComponent implements OnInit {
  title = "Verify chain"
  angForms: FormGroup[] = [];
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
    console.log(this.angForms);
  }

  createForm():void {

    this.angForms.push(this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ],
      signature: ['', Validators.required ]
   }));

   this.angForms.push(this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ],
      signature: ['', Validators.required ]
   }));

  this.angForms.push(this.fb.group({
      vendor: ['', Validators.required ],
      produce: ['', Validators.required ],
      quantity: ['', Validators.required ],
      date: ['', Validators.required ],
      signature: ['', Validators.required ]
   }));

  }

  verify(vendor, produce, quantity, date, signature) {
    this.xsignService.verify(vendor, produce, quantity, date, signature)
      .subscribe(result => this.result = JSON.parse(result));
  }

  ngOnInit() {
  }

}
