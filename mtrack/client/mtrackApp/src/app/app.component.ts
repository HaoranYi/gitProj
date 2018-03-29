import { Component, OnInit } from '@angular/core';
import { TranslateService } from './translate';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent implements OnInit {
  title = 'mTrack';
  public translatedText: string;
  public supportedLangs: any[];
  public selectedVendor: string;
  public vendors: any[];

  constructor(private _translate: TranslateService) { }

  ngOnInit() {
    // standing data
    this.supportedLangs = [
      { display: '中文', value: 'zh' },
      { display: 'English', value: 'en' },
    ];

    this.vendors = [
      'Vendor_A',
      'Vendor_B',
      'Vendor_C'
    ];

    this.selectedVendor = 'Vendor_A';

    // set current langage
    this.selectLang('zh');
  }

  isCurrentLang(lang: string) {
    // check if the selected lang is current lang
    return lang === this._translate.currentLang;
  }

  selectLang(lang: string) {
    // set current lang;
    this._translate.use(lang);
    this.refreshText();
  }

  refreshText() {
    // refresh translation when language change
    this.translatedText = this._translate.instant('hello world');
  }

  selectVendor(vendor: string) {
    console.log(vendor);
  }
}
