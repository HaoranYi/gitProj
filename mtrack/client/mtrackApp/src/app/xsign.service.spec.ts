import { TestBed, inject } from '@angular/core/testing';

import { XsignService } from './xsign.service';

describe('XsignService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [XsignService]
    });
  });

  it('should be created', inject([XsignService], (service: XsignService) => {
    expect(service).toBeTruthy();
  }));
});
