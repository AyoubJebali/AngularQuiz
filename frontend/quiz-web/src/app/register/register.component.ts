import { Component } from '@angular/core';
import { Router, RouterModule } from '@angular/router';
import { AuthService } from '../auth.service';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-register',
  standalone: true,
  imports: [FormsModule,RouterModule],
  templateUrl: './register.component.html',
  styleUrl: './register.component.css'
})
export class RegisterComponent {
  username: string = '';
  email: string = '';
  password: string = '';
  constructor(private authService: AuthService, private router: Router) {
    if (this.authService.isLoggedIn()) {
      this.router.navigate(['/home']);
    }
   }
  onRegister(): void {
    const user = {
      username: this.username,
      email: this.email,
      password: this.password,
      
    };
   
    this.authService
    .register(user)
    .then((registrationSuccess) => {
      if (registrationSuccess) {
        console.log("Registration successful!");
        this.router.navigate(['/login']);
      } else {
        console.log("Registration failed.");
      }
    })
    .catch((error) => {
      console.error("Error during registration:", error);
    });
  }
  
  

}