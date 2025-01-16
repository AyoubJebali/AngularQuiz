import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FooterComponent } from './footer/footer.component';
import { PopupGuideComponent } from './popup-guide/popup-guide.component';
import { HomeComponent } from './home/home.component';
import { HeaderComponent } from './header/header.component';
import { QuizSectionComponent } from './quiz-section/quiz-section.component';
import { MainComponent } from './main/main.component';
import { RouterModule ,  } from '@angular/router';
import { routes } from './app.routes';
import { LoginComponent } from "./login/login.component";
@Component({
  selector: 'app-root',
  imports: [RouterOutlet, FooterComponent, HeaderComponent] ,
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'quiz-web';
  isActive = false;

  toggleActiveState(): void {
    this.isActive = !this.isActive;
  }
}
