import { Component, OnInit } from '@angular/core';
import { VisibilityPopUpService } from '../visibility-pop-up.service';
import { PopupGuideComponent } from '../popup-guide/popup-guide.component';
import { QuizSectionComponent } from '../quiz-section/quiz-section.component';
import { HomeComponent } from '../home/home.component';

@Component({
  selector: 'app-main',
  imports: [PopupGuideComponent, QuizSectionComponent, HomeComponent],
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.css']
})
export class MainComponent implements OnInit {
  GuideVisible: boolean = false;
  QuizActive: boolean = false;

  constructor(private visibilityService: VisibilityPopUpService) {}

  ngOnInit(): void {
    this.visibilityService.visibility$.subscribe(isVisible => {
      this.GuideVisible = isVisible;
    });

    this.visibilityService.quizActive$.subscribe(isActive => {
      this.QuizActive = isActive;
    });
  }
}