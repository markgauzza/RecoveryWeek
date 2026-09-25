import { Routes } from '@angular/router';
import { DailySummaryComponent } from './components/daily-summary/daily-summary.component';

export const routes: Routes = [
  // home
  { path: '', component: DailySummaryComponent },

  // optional explicit path
  { path: 'daily-summary', component: DailySummaryComponent },

  // wildcard LAST only
  { path: '**', redirectTo: '' },
];