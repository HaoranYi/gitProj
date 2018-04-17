// css for validation error
.required::after {     content: " *";     color: red; }
.form-control.ng-invalid {     border-left:5px solid red; }
.form-control.ng-invalid ~ label.checkbox-inline::after {     content: " *";     color: red; }


// form group
this.sampleForm = this.formBuilder.group({
            firstName: new FormControl('', Validators.required),
            lastName: new FormControl('', Validators.required),
            email: new FormControl('', [Validators.required,Validators.pattern(this.regEmail)]),
            programmingLanguage: this.formBuilder.array([{}])
        });


// form data
class Item {
   constructor(
        private text: string,
        private value: number) { }
}
class FormControlMetadata {
   constructor(
        private checkboxName: string,
        private checkboxLabel: string,
        private associateControlName: string,
        private associateControlLabel: string,
        private associateControlType: string,
        private associateControlData: Array<Item>) { }
}
this.programmingLanguageList = [
        new Item('PHP',1),
        new Item('JavaScript',2),
        new Item('C#',3),
        new Item('Other',4)];
     this.otherProgrammingLanguageList = [
      new Item('Python',1),
      new Item('Ruby',2),
      new Item('C++',3),
      new Item('Rust',4)];
    this.phpVersionList = [
      new Item('v4',1),
      new Item('v5',2),
      new Item('v6',3),
      new Item('v7',4)];


    textbox =1 ,
    dropdown = 2,
    radioButtonList = 3
}

// plug data into form group
export class Common {
  public static ControlType = ControlType;
  public static CheckboxPrefix = 'cbLanguage_';
  public static OtherPrefix ='otherValue_';
}

langControlMetada: Array<FormControlMetadata> = [];

  populateProgrammingLanguage() {
    //get the property
    this.programmingFormArray = this.sampleForm.get('programmingLanguage') as FormArray;
    //clear
    this.programmingFormArray.removeAt(0);

    let p:Item;
    //loop through the list and create the formarray metadata
    for (p of this.programmingLanguageList) {

      let control = new FormControlMetadata();
      let group = this.formBuilder.group({});

      //create the checkbox and other form element metadata
      control.checkboxName = `${Common.CheckboxPrefix}${p.value}`;
      control.checkboxLabel = p.text;
      control.associateControlName = `${Common.OtherPrefix}${p.value}`;
      control.associateControlLabel = `${p.text} comments`;
      control.associateControlType = Common.ControlType[Common.ControlType.textbox];

      //assume 1 is radio button list
       if (p.value == 1) {
          control.associateControlType = Common.ControlType[Common.ControlType.radioButtonList];
          control.associateControlData = this.phpVersionList;
      }

      //just assumed id 4 is dropdown
      if (p.value == 4) {
          control.associateControlType = Common.ControlType[Common.ControlType.dropdown];
          control.associateControlData = this.otherProgrammingLanguageList;
      }

      //store in array, use by html to loop through
      this.langControlMetada.push(control);

      //form contol
      let checkBoxControl = this.formBuilder.control('');
      let associateControl = this.formBuilder.control({ value: '', disabled: true });

      //add to form group [key, control]
      group.addControl(`${Common.CheckboxPrefix}${p.value}`, checkBoxControl);
      group.addControl(`${Common.OtherPrefix}${p.value}`, associateControl);

      //add to form array
      this.programmingFormArray.push(group);
    }


// html template
<div class="form-group row" formArrayName="programmingLanguage">
        <div class="col-xs-12"
             *ngFor="let item of langControlMetada; let i = index;">
            <div [formGroupName]="i">
                <div class="form-group row">
                    <div class="form-inline" style="margin-left:15px;">
                        <div class="form-check">
                            <label [for]="item.checkboxName" class="form-check-label">
                                <input type="checkbox" class="form-check-input" [id]="item.checkboxName"
                                        (change)="languageSelectionChange(i, item.checkboxName, item.associateControlName)"
                                        [formControlName]="item.checkboxName"> {{ item.checkboxLabel}}
                            </label>
                            <input *ngIf="item.associateControlType == 'textbox'"
                                   class="form-control form-control-sm"
                                   id="item.associateControlName"
                                   [placeholder]="item.associateControlLabel" maxlength="255"
                                   [formControlName]="item.associateControlName" />
                            <span *ngIf="item.associateControlType == 'dropdown'">
                                <select class="form-control form-control-sm"
                                        [formControlName]="item.associateControlName">
                                    <option *ngFor="let item of item.associateControlData"
                                            [value]="item.value">
                                        {{item.text}}
                                    </option>
                                </select>
                            </span>
                            <span *ngIf="item.associateControlType == 'radioButtonList'">
                                <span *ngFor="let option of item.associateControlData">
                                    <input #version type="radio" [formControlName]="item.associateControlName"
                                           class="form-control form-control-sm"
                                           [value]="option.value">
                                    <label class="checkbox-inline" *ngIf="!version.disabled"> {{option.text}}</label>
                                </span>
                            </span>
                        </div>
                    </div>
                 </div>
             </div>
      </div>


// hide/show form control based on selection
languageSelectionChange(pos: number, cnkName: string, txtName: string) {
  let programmingLanguage = this.programmingLanguages();

  let control = programmingLanguage.controls[pos] as FormGroup

  if (control.controls[cnkName].value == true) {
      //checkbox checked
      control.controls[txtName].enable();
      control.controls[txtName].setValidators([Validators.required]);
      control.controls[txtName].updateValueAndValidity();
      this.selectedLanguageCount++;
  }
  else {
      //unchecked
      control.controls[txtName].setValue('');
      control.controls[txtName].disable();
      control.controls[txtName].clearValidators();
      control.controls[txtName].updateValueAndValidity();
      this.selectedLanguageCount--;
  }
}


// get the data from the form
programmingLanguages(): FormArray {
    return this.sampleForm.get('programmingLanguage') as FormArray;
  };

public submit(e: any): void {
    e.preventDefault();

    //reset
    let selectedLanguageList: Array<Item> = [];
    let programmingLanguage = this.programmingLanguages();
    let i: number;
    //checkbox id
    let languageId: number = 0;

    for(i = 0; i < programmingLanguage.controls.length; i++) {

        let control = programmingLanguage.controls[i] as FormGroup
        let selectedLanguage: Language = {} as any;

        //get the selected checkbox id
        for (var k in control.controls) {
            languageId = Number(k.replace(/[a-zA-Z_]/g, ""));
            break;
        }

        //capture the selected checkbox Id and textbox value
        if (control.controls[`${Common.CheckboxPrefix}${languageId}`].value == true) {
            selectedLanguage.value = languageId;
            selectedLanguage.text = control.controls[`${Common.OtherPrefix}${languageId}`].value
            selectedLanguageList.push(selectedLanguage);
        }
    }

    if (selectedLanguageList.length == 0) {
        this.missingLanguage = true;
    } else {
        //submit to API
        let formObjectToApi = new FormControlMetadata();

        formObjectToApi.lastName = this.sampleForm.controls['lastName'].value;
        formObjectToApi.firstName = this.sampleForm.controls['firstName'].value;
        formObjectToApi.email = this.sampleForm.controls['email'].value;
        formObjectToApi.selectedLanguages = selectedLanguageList;

        this.missingLanguage = false;
        this.test = formObjectToApi;
    }
