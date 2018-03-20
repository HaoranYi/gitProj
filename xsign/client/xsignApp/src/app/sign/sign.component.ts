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
  svg: string = "";

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
      .subscribe(result => {
        console.log(result);
        this.result = JSON.parse(result);
        //this.result = jj.signature;
        //this.svg = jj.svg;
        //let x = JSON.parse(result).signature;
        //let s = 0;
        //var sliced = [];
        //while (s + 40 < x.length) {
        //  sliced.push(x.slice(s, s+40));
        //  s +=40;
        //}
        //this.result = sliced;
        //console.log(this.result);
      }
      );
  }

  ngOnInit() {
    //this.route.params.subscribe(params => {
    //  this.coin = this.service.editCoin(params['id']).subscribe(res => {
    //    this.coin = res;
    //  });
    //});
  }
}

