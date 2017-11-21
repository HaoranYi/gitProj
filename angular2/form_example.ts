/**
 * code example to build forms with angular.
 * core class: FormGroup/FormControl. A FormGroup can be nested inside
 *             FormGroup.
 * core directives: formGroup, formGroupName, formControlName.
 * use those directives to bind html element to model defined by
 * FormGroup/FormControl.
 */
import {
    NgModel,
    Component,
    Pipe,
    OnInit
} from '@angular/core';
import {
    ReactiveFormsModule,
    FormsModule,
    FormGroup,
    FormControl,
    Validators,
    FormBuilder
} from '@angular/forms';
import {BrowserModule} from '@angular/platform-browser';
import {platformBrowserDynamic} from '@angular/platform-browser-dynamic';

@Component({
    selector: 'model-form',
    template: `<!--supress All -->
<form novalidate [formGroup]="myform">
<fieldset formGroupName="name">
    <div class="form-group">
        <label>First Name</label>
        <input type="text" class="form_control" formControlName="firstName">
    </div>

    <div class="form-group">
        <label>Last Name</label>
        <input type="text" class="form_control" formControlName="lastName">
    </div>
</fieldset>

<div class="form-group">
    <label>Email</label>
    <input type="email" class="form_control" formControlName="email">
</div>

<div class="form-group">
    <label>Password</label>
    <input type="password" class="form_control" formControlName="password">
</div>

<div class="form-group">
    <label>Language</label>
    <select class="form-control" formControlName="language">
        <option value="">please select a language </option>
        <option *ngFor="let x of langs" [value]="lang">{{lang}}</option>
    </select>
</div>

<pre>{{myform.value | json}}</pre>
`
})
class ModelFormComponnet implements OnInit {
    langs: string[] = [
        'English',
        'Franch',
        'German',
    ];
    myform: FormGroup;

    ngOnInit() {
        this.myform = new FormGroup({
            name: new FormGroup({
                firstName: new FormControl('', Validators.required),
                lastName: new FormControl('', Validators.required),
            }),
            email: new FormControl('', [Validators.required,
                validators.pattern("[^ @]*@[^ @]*")]
            ),
            passowrd: new FormControl('', [Validators.required,
                validators.minLength(8)]
            ),
            language: new FormControl()
        });
    }
}

@Component({
    selector: 'app',
    template: `<model-form></model-form>`
})
class AppComponent {
}

@NgModule({
    imports: [
        BrowserModule,
        FormsModule,
        ReactiveFormsModule],
    declarations: [
        AppComponent,
        ModelFormComponent
    ],
    bootstrap: [
        AppComponent
    ],
})
class AppModule {
}

platformBrowserDynamic().bootstrapModule(AppModule);
