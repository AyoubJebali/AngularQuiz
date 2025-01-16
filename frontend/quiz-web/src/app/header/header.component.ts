import { Component, OnInit } from '@angular/core';
import { Router, NavigationEnd } from '@angular/router';
import { filter } from 'rxjs/operators';
import { AuthService } from '../auth.service';

@Component({
  selector: 'app-header',
  standalone: true,
  imports: [],
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.css']
})
export class HeaderComponent implements OnInit {
  currentRoute: string = '';
  logoutText: string = 'Login';

  constructor(private authService: AuthService, private router: Router) {
    this.authService.authStatus$.subscribe(() => {
      this.updateLogoutText();
    }
    );
    this.router.events.pipe(
      filter(event => event instanceof NavigationEnd)
    ).subscribe((event: NavigationEnd) => {
      this.currentRoute = event.urlAfterRedirects;
    });
  }

  ngOnInit(): void {
    this.updateLogoutText();
    
  }

  updateLogoutText(): void {
    this.logoutText = this.authService.isLoggedIn() ? 'Logout' : 'Login';
  }

  logout(): void {
    if (this.authService.isLoggedIn()) {
      this.authService.logout();
      this.router.navigate(['/login']);
    } else {
      this.router.navigate(['/login']);
    }
  }

  
}