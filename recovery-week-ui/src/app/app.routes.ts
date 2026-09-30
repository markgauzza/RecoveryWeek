import { Routes } from '@angular/router';
import { DailySummaryComponent } from './components/daily-summary/daily-summary.component';
import { ReportsComponent } from './components/reports/reports.component';


export const routes: Routes = [
  // home
  { path: '', component: DailySummaryComponent },

  // optional explicit path
  { path: 'daily-summary', component: DailySummaryComponent },
  { path: 'reports', component: ReportsComponent },


  // wildcard LAST only
  { path: '**', redirectTo: '' },
];