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

const routes: Routes = [
  { path: 'sign', component: SignComponent },
  { path: 'verify', component: VerifyComponent },
  { path: 'chain', component: ChainComponent },
  { path: '', redirectTo: '/track', pathMatch: 'full'},
  { path: 'track', component: TrackComponent },
  { path: 'sell', component: SellComponent },
  { path: 'confirm', component: ConfirmComponent },
  { path: 'history', component: HistoryComponent },
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
