import { Component, OnInit } from '@angular/core';
import { QuizService } from '../quiz.service';
interface LeaderboardEntry {
  username: string;
  score: number;
}
@Component({
  selector: 'app-leaderboard',
  imports: [],
  templateUrl: './leaderboard.component.html',
  styleUrl: './leaderboard.component.css'
})
export class LeaderboardComponent implements OnInit {
  leaderboard: LeaderboardEntry[] = [];
  constructor(private quizService: QuizService) {}
  ngOnInit(): void {
    this.quizService.getLeaderboard().subscribe(
      (data) => {
        this.leaderboard = data;
        console.log(data);  // Process the leaderboard data
      },
      (error) => {
        console.error('Error fetching leaderboard:', error);
      }
    );
  }
  

}
