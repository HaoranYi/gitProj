import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { FormGroup,  FormBuilder,  Validators } from '@angular/forms';
import { XsignService } from '../xsign.service';

@Component({
  selector: 'app-login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent implements OnInit {

  title = "Sign in";
  angForm: FormGroup;
  result: any;

  constructor(private route: ActivatedRoute, private router: Router, private fb: FormBuilder, private xsignService: XsignService) {
    this.createForm();
   }

  // TODO: make it a dynamic form
  createForm() {
    this.angForm = this.fb.group({
      user: ['', Validators.required ],
      pwd: ['', Validators.required ],
   });
  }

  signIn(user, pwd) {
    // TODO
    console.log(user, pwd);
  }

  ngOnInit() {
    // TODO
  }
}

