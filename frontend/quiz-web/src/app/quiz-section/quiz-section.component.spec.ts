import { ComponentFixture, TestBed } from '@angular/core/testing';

import { QuizSectionComponent } from './quiz-section.component';

describe('QuizSectionComponent', () => {
  let component: QuizSectionComponent;
  let fixture: ComponentFixture<QuizSectionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [QuizSectionComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(QuizSectionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
