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
import { AdministratorComponent } from './administrator/administrator.component';
import { ManufacturerComponent } from './manufacturer/manufacturer.component';
import { DealerComponent } from './dealer/dealer.component';
import { ConsumerComponent } from './consumer/consumer.component';
import { LoginComponent } from './login/login.component';
import { CertificateComponent } from './certificate/certificate.component';
import { MedicineComponent } from './medicine/medicine.component';

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
    HistoryComponent,
    AdministratorComponent,
    ManufacturerComponent,
    DealerComponent,
    ConsumerComponent,
    LoginComponent,
    CertificateComponent,
    MedicineComponent
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

