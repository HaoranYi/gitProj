Client webapp for xsign

npm3.3.6
@angular/cli1.73


Example to create login
http://jasonwatmore.com/post/2016/09/29/angular-2-user-registration-and-login-example-tutorial

Alert service to display alert message
Login service to authenticate the user
Use guard on routes to guard route url on client
Use jwt token to guard on the server
Use HttpInterceptor to add jwt token to http header
  >(add "useClass" for service provider)
Use FakeBackendInterceptor implements HttpInterceptor
  > add to provider; in client code calls /api/authenticate

use ngForm for two way binding

<div class="col-md-6 col-md-offset-3">
    <h2>Login</h2>
    <form name="form" (ngSubmit)="f.form.valid && login()" #f="ngForm" novalidate>
        <div class="form-group" [ngClass]="{ 'has-error': f.submitted && !username.valid }">
            <label for="username">Username</label>
            <input type="text" class="form-control" name="username" [(ngModel)]="model.username" #username="ngModel" required />
            <div *ngIf="f.submitted && !username.valid" class="help-block">Username is required</div>
        </div>
        <div class="form-group" [ngClass]="{ 'has-error': f.submitted && !password.valid }">
            <label for="password">Password</label>
            <input type="password" class="form-control" name="password" [(ngModel)]="model.password" #password="ngModel" required />
            <div *ngIf="f.submitted && !password.valid" class="help-block">Password is required</div>
        </div>
        <div class="form-group">
            <button [disabled]="loading" class="btn btn-primary">Login</button>
            <img *ngIf="loading" src="..."
            <a [routerLink]="['/register']" class="btn btn-link">Register</a>
        </div>
    </form>
</div>
