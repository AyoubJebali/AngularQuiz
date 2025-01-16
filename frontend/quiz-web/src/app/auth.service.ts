import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, BehaviorSubject } from 'rxjs';
import { tap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private apiUrl = 'http://localhost:5000'; // Replace with your backend URL
  private tokenKey = 'authToken'; // Key to store the token in localStorage
  private authStatus = new BehaviorSubject<boolean>(this.isLoggedIn());
  authStatus$ = this.authStatus.asObservable();
  private usersKey = 'users'; 
  private loggedInKey = 'loggedInUser'; 
  constructor(private http: HttpClient) {}
  
  /**
   * Login method to authenticate the user.
   * @param credentials - Object containing email and password.
   */
  async login(credentials: { username: string; password: string }): Promise<boolean> {
    try {
      const response = await this.http.post<any>(`${this.apiUrl}/login`, credentials).toPromise();
  
      if (response) {
        console.log(response);
        localStorage.setItem(this.loggedInKey, response.username);
        localStorage.setItem(this.tokenKey, this.getCookie('session'));
        console.log('Login successful:', response);
        return true;
      }
  
      console.error('Login failed:', response);
      return false;
    }catch (error) {
      console.error('Error during login:', error);
      return false;
  }
}
  async register(user: { username: string , email: string; password: string;  }): Promise<boolean> {
    try {
     
      const response = await this.http.post<any>(`${this.apiUrl}/register`, user).toPromise();
  
      if (!response) {
        console.error('Registration failed');
        return false;
      }
  
      console.log('User registered successfully!');
      return true;
    } catch (error) {
      console.error('Error during registration:', error);
      return false;
    }
  }
  
  /**
   * Logout method to clear the user's authentication token.
   */
  logout(): void {
    localStorage.removeItem(this.loggedInKey);
    localStorage.removeItem(this.tokenKey);
    this.authStatus.next(false);
  }

   getCookie(name: string): string  {
    console.log(document.cookie);
    const value = `; ${document}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop()?.split(';').shift() || "null";
    return "null";
  }
  /**
   * Check if the user is authenticated by verifying if the token exists.
   */
  isLoggedIn(): boolean {
    return !!localStorage.getItem(this.loggedInKey);
  }

  /**
   * Get the authentication status as an observable.
   */
  getAuthStatus(): Observable<boolean> {
    return this.authStatus.asObservable();
  }

  /**
   * Get the current user's token.
   */
  getToken(): string | null {
    return localStorage.getItem(this.tokenKey);
  }
}
