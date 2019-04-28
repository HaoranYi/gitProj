import { Component } from '@angular/core';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.css']
})
export class AppComponent {
  title = 'tabapp';

  /**
   * this exmaple use <mat-tab-group> to show static tab content inline.
   * We could use routeLinks and <md-tab-nav-bar> together to integrate tab nav with route map.
   */
}
