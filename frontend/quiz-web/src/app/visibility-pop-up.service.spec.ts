import { TestBed } from '@angular/core/testing';

import { VisibilityPopUpService } from './visibility-pop-up.service';

describe('VisibilityPopUpService', () => {
  let service: VisibilityPopUpService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(VisibilityPopUpService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
