import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormsModule } from '@angular/forms';


@Component({
  selector: 'app-login',
  standalone: true,
  imports: [FormsModule],
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.css']
})
export class LoginComponent {
  username: string = '';
  password: string = '';

  constructor(private authService: AuthService, private router: Router) { 
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/home']);
    }
  }

  async onLogin(): Promise<void> {
    try {
      const loginSuccess = await this.authService.login({
        username: this.username,
        password: this.password,
      });
  
      if (loginSuccess) {
        console.log('Login successful');
        this.router.navigate(['/home']);
      } else {
        alert('Invalid email or password');
      }
    } catch (error) {
      console.error('Error during login:', error);
      alert('An error occurred. Please try again later.');
    }
  }
  
  navigateToRegister(): void {
    this.router.navigate(['/register']);
  }
}