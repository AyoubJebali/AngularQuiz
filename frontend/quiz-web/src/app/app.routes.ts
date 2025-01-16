import { Routes } from '@angular/router';
import { LoginComponent } from './login/login.component';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { MainComponent } from './main/main.component';
import { RegisterComponent } from './register/register.component';
import { AuthGuard } from './auth.guard';
import { LeaderboardComponent } from './leaderboard/leaderboard.component';
export const routes: Routes = [
    { path: 'home', component: MainComponent , canActivate: [AuthGuard] },
    { path: 'leaderboard', component: LeaderboardComponent , canActivate: [AuthGuard] },
    { path: 'login', component: LoginComponent },
    { path: 'register', component: RegisterComponent },
    { path: '', redirectTo: '/home', pathMatch: 'full' },
    { path: '**', component: MainComponent , canActivate: [AuthGuard] },];
