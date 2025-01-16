import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class VisibilityPopUpService {
  private visibilitySubject = new BehaviorSubject<boolean>(false);
  visibility$ = this.visibilitySubject.asObservable();

  private quizActiveSubject = new BehaviorSubject<boolean>(false);
  quizActive$ = this.quizActiveSubject.asObservable();

  setVisibility(isVisible: boolean) {
    this.visibilitySubject.next(isVisible);
  }

  getVisibility(): boolean {
    return this.visibilitySubject.value;
  }

  setQuizActive(isActive: boolean) {
    this.quizActiveSubject.next(isActive);
  }

  getQuizActive(): boolean {
    return this.quizActiveSubject.value;
  }
}