import { Component, OnInit } from '@angular/core';
import { QuizService } from '../quiz.service';
import { VisibilityPopUpService } from '../visibility-pop-up.service';
import { NgFor } from '@angular/common';

@Component({
  selector: 'app-quiz-section',
  templateUrl: './quiz-section.component.html',
  styleUrls: ['./quiz-section.component.css'],
})
export class QuizSectionComponent implements OnInit {
  question: string = '';
  options: string[] = [];
  score: number = 0;
  currentIndexOfQuestion: number = 1;
  isQuizActive: boolean = false;
  ShowResults: boolean = false;
  totalQuestions: number = 0;
  btnActive: boolean = false;
  questionStates: (boolean | null)[] = [];
  diableAllOptions: boolean = false;
  progressValue: number = 0;
  constructor(private quizService: QuizService, private visibilityService: VisibilityPopUpService) { }

  ngOnInit(): void {

    this.quizService.getQuizzes();
    this.visibilityService.quizActive$.subscribe(isActive => {
      this.isQuizActive = isActive;
      if (this.isQuizActive) {

        this.loadQuestion();
        this.updateScore();
        this.totalQuestions = this.quizService.getTotalQuestions();
      }
    });

    this.quizService.score$.subscribe(score => {
      this.score = score;
    });
  }

  loadQuestion(): void {
    const currentQuestion = this.quizService.getCurrentQuestion();
    this.question = currentQuestion.question;
    this.options = currentQuestion.options;
  }

  selectOption(index: number): void {
    if (!this.diableAllOptions) {
      let correctIndex: number = this.quizService.getCorrectAnswerIndex();
      const isCorrect = this.quizService.checkAnswer(index);
      this.btnActive = true;
      this.diableAllOptions = true;
      if (isCorrect) {
        this.questionStates[index] = true;
        this.updateScore();
      } else {
        this.questionStates[index] = false;
        this.questionStates[correctIndex] = true;
      }
    }
  }

  finishQuiz(): void {
    this.visibilityService.setQuizActive(false); // Optionally deactivate the quiz
    this.quizService.getQuizzes();
    this.resetQuiz();
  }
  loadNextQuestion(): void {
    if (this.quizService.isQuizOver()) {
      this.saveScore();
      this.progressValue = this.score / this.totalQuestions * 100;
      this.ShowResults = true;
    } else {
      this.currentIndexOfQuestion++;
      this.loadQuestion();
      this.resetQuestionStates(); // Reset the question states after loading the next question
    }
    this.btnActive = false;
  }
  getProgressStyle(): string {
    return `conic-gradient(#AA2C86 ${this.progressValue * 3.6}deg, rgba(255, 255, 255, .1) 0deg)`;
  }
  updateScore(): void {
    this.score = this.quizService.getScore();
  }
  tryAgain(): void {
    this.ShowResults = false;
    this.resetQuiz();
    this.quizService.getQuizzes();
  }

  resetQuiz(): void {
    this.quizService.resetQuiz();
    this.question = '';
    this.options = [];
    this.score = 0;
    this.currentIndexOfQuestion = 1;
    this.isQuizActive = false;
    this.ShowResults = false;
    this.diableAllOptions = false;
    this.questionStates = new Array(this.totalQuestions).fill(null); // Reset the question states
  }

  resetQuestionStates(): void {
    this.diableAllOptions = false;
    this.questionStates = new Array(this.totalQuestions).fill(null); // Reset the question states after each question
  }
  getOptionClass(index: number): string {
    let classes = 'option';
    if (this.questionStates[index] === true) {
      classes += ' correct';
    } else if (this.questionStates[index] === false) {
      classes += ' incorrect';
    }
    return classes;
  }
  saveScore(): void {
    console.log('Saving score...');
    let username: string = localStorage.getItem('loggedInUser') as string;
    this.quizService.saveScore(username);
  }
}