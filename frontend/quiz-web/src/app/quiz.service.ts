import { Injectable } from '@angular/core';
import { BehaviorSubject,Observable  } from 'rxjs';
import { HttpClient, HttpParams } from '@angular/common/http';
import { tap } from 'rxjs/operators';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
interface LeaderboardEntry {
  username: string;
  score: number;
}
@Injectable({
  providedIn: 'root'
})

export class QuizService {
  private questions: { question: string; options: string[]; correctIndex: number }[] = [];
  private apiUrl = 'http://localhost:5000/';  // URL of the Flask endpoint
  constructor(private http: HttpClient) {  }
  categeoryIds: number[] = [1,2,3,4,5];
  // Method to get quizzes by category IDs
  getQuizzes(): void {
    const params = new HttpParams().set('category_ids', this.categeoryIds.join(','));
     this.http.get<any>(this.apiUrl+"/quizzes", { params }).subscribe( data => { 
      this.questions = data.map((question: any) => ({
        question: question.question, 
        options: question.options,
        correctIndex: question.correctIndex
      }));
     });
      
      // When the response is received, update the questions array
      // tap(response => {
      //   console.log(response);
      //   this.questions = response.map((question: any) => ({
      //     question: question.question, 
      //     options: question.options,
      //     correctIndex: question.correctIndex
      //   }));
      // })
    
  }
  private currentIndex = 0;
  private scoreSubject = new BehaviorSubject<number>(0);
  score$ = this.scoreSubject.asObservable();

  getCurrentQuestion() {
    return this.questions[this.currentIndex];
  }

  checkAnswer(selectedIndex: number): boolean {
    const isCorrect = this.questions[this.currentIndex].correctIndex === selectedIndex;
    if (isCorrect) {
      this.scoreSubject.next(this.scoreSubject.value + 1);
    }
    this.currentIndex++;
    return isCorrect;
  }
  getCorrectAnswerIndex(): number {
    return this.questions[this.currentIndex].correctIndex;
  }

  getTotalQuestions(): number {
    return this.questions.length;
  }
  getScore(): number {
    return this.scoreSubject.value;
  }

  isQuizOver(): boolean {
    return this.currentIndex >= this.questions.length;
  }

  resetQuiz(): void {
    this.currentIndex = 0;
    this.scoreSubject.next(0);
  }

  saveScore(username: string): void{
     this.http.post(`${this.apiUrl}/saveScore`, {
      username,
      score: this.scoreSubject.value,
    }).subscribe(
      response => {
        console.log('Score saved:', response);
      },
      error => {
        console.error('Error saving score:', error);
        if (error.status === 400) {
          console.log('Bad request:', error.error);  // Check error details
        }
      }
    );
  }
  
  getLeaderboard(): Observable<LeaderboardEntry[]> {
    return this.http.get<LeaderboardEntry[]>(`${this.apiUrl}/leaderboard`);
  }
  
  
}