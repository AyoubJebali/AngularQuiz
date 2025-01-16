import { Component } from '@angular/core';
import { VisibilityPopUpService } from '../visibility-pop-up.service';

@Component({
  selector: 'app-popup-guide',
  templateUrl: './popup-guide.component.html',
  styleUrls: ['./popup-guide.component.css']
})
export class PopupGuideComponent {
  isVisible: boolean = false;

  constructor(private visibilityService: VisibilityPopUpService) {
    this.visibilityService.visibility$.subscribe(isVisible => {
      this.isVisible = isVisible;
    });
  }

  toggleVisibility() {
    this.isVisible = !this.isVisible;
    this.visibilityService.setVisibility(this.isVisible);
  }
  toggleQuizActive() {
    this.toggleVisibility();
    const currentQuizActiveState = this.visibilityService.getQuizActive();
    this.visibilityService.setQuizActive(!currentQuizActiveState);
  }
}