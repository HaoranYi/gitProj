import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';
import { ReactiveFormsModule } from '@angular/forms';
import { FormsModule } from '@angular/forms';

import { AppComponent } from './app.component';
import { SignComponent } from './sign/sign.component';
import { VerifyComponent } from './verify/verify.component';
import { AppRoutingModule } from './/app-routing.module';
import { XsignService } from './xsign.service';
import { VendorService } from './vendor.service';

import { ChainComponent } from './chain/chain.component';

import { TRANSLATION_PROVIDERS, TranslatePipe, TranslateService } from './translate';
import { TrackComponent } from './track/track.component';
import { SellComponent } from './sell/sell.component';
import { ConfirmComponent } from './confirm/confirm.component';
import { HistoryComponent } from './history/history.component';
import {DatePipe} from '@angular/common';

@NgModule({
  declarations: [
    TranslatePipe,
    AppComponent,
    SignComponent,
    VerifyComponent,
    ChainComponent,
    TrackComponent,
    SellComponent,
    ConfirmComponent,
    HistoryComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    ReactiveFormsModule,
    FormsModule

  ],
  providers: [DatePipe, XsignService, VendorService, TRANSLATION_PROVIDERS, TranslateService],
  bootstrap: [AppComponent]
})
export class AppModule { }

