import {
  Component,
  afterNextRender,
  inject,
  ChangeDetectorRef,
  NgZone,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { finalize } from 'rxjs/operators';
import { WorkoutService } from '../../services/workout';
import { ReportsService } from '../../services/reports.service';
import { WorkoutDayOfWeekReportRow } from '../../models/workout-day-of-week-report';

@Component({
  selector: 'app-workout-by-day-report',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './workout-by-day-report.component.html',
  styleUrl: './workout-by-day-report.component.css',
})
export class WorkoutByDayReportComponent {
  private cdr = inject(ChangeDetectorRef);
  private zone = inject(NgZone);
  private reportsService = inject(ReportsService);

  rows: WorkoutDayOfWeekReportRow[] = [];
  loading = false;
  error: string | null = null;

  readonly columns = [
    'Workout',
    'Sunday',
    'Monday',
    'Tuesday',
    'Wednesday',
    'Thursday',
    'Friday',
    'Saturday',
    'Odd',
    'Even',
  ] as const;

  constructor(private workoutService: WorkoutService) {
    afterNextRender(() => this.load());
  }

  load(): void {
    this.loading = this.rows.length === 0;
    this.error = null;
    this.cdr.detectChanges();

    this.reportsService
      .getWorkoutsByDayOfWeek()
      .pipe(
        finalize(() => {
          this.zone.run(() => {
            this.loading = false;
            this.cdr.detectChanges();
          });
        })
      )
      .subscribe({
        next: (data) => {
          this.zone.run(() => {
            this.rows = data ?? [];
            this.cdr.detectChanges();
          });
        },
        error: (err) => {
          this.zone.run(() => {
            console.error(err);
            this.error = err.message || 'Failed to load report';
            this.cdr.detectChanges();
          });
        },
      });
  }

  cellValue(row: WorkoutDayOfWeekReportRow, col: string): string | number {
    return (row as any)[col] ?? 0;
  }
}