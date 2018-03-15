import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { SignComponent } from './sign/sign.component';
import { VerifyComponent } from './verify/verify.component';
import { AppRoutingModule } from './/app-routing.module';
import { XsignService } from './xsign.service';

@NgModule({
  declarations: [
    AppComponent,
    SignComponent,
    VerifyComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule, 
    ReactiveFormsModule
  ],
  providers: [XsignService],
  bootstrap: [AppComponent]
})
export class AppModule { }
