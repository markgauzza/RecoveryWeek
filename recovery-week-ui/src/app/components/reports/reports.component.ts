import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WorkoutByDayReportComponent } from './workout-by-day-report.component';

type ReportTab = 'by-day' | 'other'; // extend as you add reports

@Component({
  selector: 'app-reports',
  standalone: true,
  imports: [CommonModule, WorkoutByDayReportComponent],
  templateUrl: './reports.component.html',
  styleUrl: './reports.component.css',
})
export class ReportsComponent {
  activeTab: ReportTab = 'by-day';

  selectTab(tab: ReportTab): void {
    this.activeTab = tab;
  }
}