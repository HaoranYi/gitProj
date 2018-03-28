import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Routes } from '@angular/router';

import { SignComponent } from './sign/sign.component';
import { VerifyComponent } from './verify/verify.component';
import { ChainComponent } from './chain/chain.component';

const routes: Routes = [
  { path: 'sign', component: SignComponent },
  { path: 'verify', component: VerifyComponent },
  { path: 'chain', component: ChainComponent },
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
