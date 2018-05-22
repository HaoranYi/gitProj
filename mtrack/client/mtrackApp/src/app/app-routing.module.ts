import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { SignComponent } from './sign/sign.component';
import { VerifyComponent } from './verify/verify.component';
import { ChainComponent } from './chain/chain.component';

import { TrackComponent } from './track/track.component';
import { SellComponent } from './sell/sell.component';
import { ConfirmComponent } from './confirm/confirm.component';
import { HistoryComponent } from './history/history.component';

import { LoginComponent } from './login/login.component';
import { DealerComponent } from './dealer/dealer.component';
import { ManufacturerComponent } from './manufacturer/manufacturer.component';
import { ConsumerComponent } from './consumer/consumer.component';
import { AdministratorComponent } from './administrator/administrator.component';
import { CertificateComponent } from './certificate/certificate.component';
import { MedicineComponent } from './medicine/medicine.component';

const routes: Routes = [
  { path: 'sign', component: SignComponent },
  { path: 'verify', component: VerifyComponent },
  { path: 'chain', component: ChainComponent },

  { path: '', redirectTo: '/track', pathMatch: 'full'},
  { path: 'track', component: TrackComponent },
  { path: 'sell', component: SellComponent },
  { path: 'confirm', component: ConfirmComponent },
  { path: 'history', component: HistoryComponent },

  { path: 'login', component: LoginComponent },
  { path: 'dealer', component: DealerComponent,
    children:[
      { path: '', redirectTo: 'track', pathMatch: 'full' },
      { path: 'track', component: TrackComponent },
      { path: 'sell', component: SellComponent },
      { path: 'confirm', component: ConfirmComponent },
      { path: 'history', component: HistoryComponent },
    ]
  },
  { path: 'consumer', component: ConsumerComponent,
    children:[
      { path: '', redirectTo: 'track', pathMatch: 'full' },
      { path: 'track', component: TrackComponent },
      { path: 'confirm', component: ConfirmComponent },
      { path: 'history', component: HistoryComponent },
    ]
  },
  { path: 'manufacturer', component: ManufacturerComponent,
    children:[
      { path: '', redirectTo: 'medicine', pathMatch: 'full' },
      { path: 'medicine', component: MedicineComponent },
      { path: 'track', component: TrackComponent },
      { path: 'sell', component: SellComponent },
      { path: 'history', component: HistoryComponent },
    ]
  },
  { path: 'administrator', component: AdministratorComponent,
    children:[
      { path: '', redirectTo: 'certificate', pathMatch: 'full' },
      { path: 'certificate', component: CertificateComponent },
      { path: 'track', component: TrackComponent },
    ]
  },
];

@NgModule({
  imports: [
    CommonModule,
    RouterModule.forRoot(routes)
  ],
  exports: [
    RouterModule
  ],
  declarations: []
})
export class AppRoutingModule { }
