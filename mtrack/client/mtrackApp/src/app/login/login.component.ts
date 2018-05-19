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
  roles = ["Administrator", "Manufacturer", "Vendor", "Consumer"];
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
      role: ['', Validators.required],
   });
  }

  signIn(user, pwd, role) {
    // TODO
    console.log(user, pwd, role);
    if (role == "Administrator"){
      this.router.navigate(['/administrator', user])
    } 
    else if (role == "Manufacturer")
    {
      this.router.navigate(['/manufacturer', user])
    }
    else if (role == "Vendor")
    {
      this.router.navigate(['/vendor', user])
    }
    else if (role == "Consumer")
    {
      this.router.navigate(['/consumer', user])
    }
  }

  ngOnInit() {
    // TODO
  }
}

