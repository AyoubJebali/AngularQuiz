import { Component } from '@angular/core';
import { VisibilityPopUpService } from '../visibility-pop-up.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent {
  clickedStart = false;

  constructor(private visibilityService: VisibilityPopUpService) {
    this.visibilityService.visibility$.subscribe(isVisible => {
      this.clickedStart = isVisible;
    });
  }

  onStartQuiz(): void {
    this.clickedStart = !this.clickedStart;
    this.visibilityService.setVisibility(this.clickedStart);
  }
}