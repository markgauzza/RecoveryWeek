import {
  Component,
  ChangeDetectorRef,
  NgZone,
  signal,
  OnInit, inject, PLATFORM_ID, afterNextRender
} from '@angular/core';

import { CommonModule } from '@angular/common';
import { WorkoutService } from '../../services/workout';
import { WorkoutDailySummary } from '../../models/workout-daily-summary';
import { PaginatedDailySummary } from '../../models/paginated-daily-summary';
import { WorkoutFormComponent } from '../workout-form/workout-form.component';
import { isPlatformBrowser } from '@angular/common';
import { finalize } from 'rxjs/operators';


@Component({
  selector: 'app-daily-summary',
  standalone: true,
  imports: [CommonModule, WorkoutFormComponent],
  templateUrl: './daily-summary.component.html',
  styleUrl: './daily-summary.component.css',
})
export class DailySummaryComponent implements OnInit {
  private platformId = inject(PLATFORM_ID);
  private workoutService = inject(WorkoutService);
  private ngZone = inject(NgZone);

  showForm = false;
  summaries = signal<WorkoutDailySummary[]>([]);
  total = 0;
  loading = false;
  error: string | null = null;

  skip = signal<number>(0);
  limit = signal<number>(30);

  constructor() { }

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {

      this.loadSummaries();

    }
  }

  toggleForm(): void {
    this.showForm = !this.showForm;
  }

  onWorkoutSaved(): void {
    this.showForm = false;
    this.loadSummaries();
  }

  onFormCancelled(): void {
    this.showForm = false;
  }

  loadSummaries(): void {
    this.loading = true;
    this.error = null;

    this.workoutService.getDailySummaries(this.skip(), this.limit())
      .pipe(
        finalize(() => {
          this.loading = false;
          // console.log('finalize loading=', this.loading, 'rows=', this.summaries.length);
        })
      )
      .subscribe({
        next: (data) => {
          console.log('daily-summary response', data);
          this.summaries.set(data?.items ?? []);
          this.total = data?.total ?? 0;

        },
        error: (err) => {
          console.error('daily-summary error', err);
          this.error = err.message || 'Failed to load daily summaries';
          this.summaries.set([]);
        }
      });
  }

  nextPage(): void {
    this.skip.set(this.skip() + this.limit());
    this.loadSummaries();
  }

  prevPage(): void {
    this.skip.set(Math.max(0, this.skip() - this.limit()));
    this.loadSummaries();
  }
}