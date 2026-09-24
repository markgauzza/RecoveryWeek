import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { WorkoutService } from '../../services/workout';
import { WorkoutDailySummary } from '../../models/workout-daily-summary';
import { PaginatedDailySummary } from '../../models/paginated-daily-summary';

@Component({
  selector: 'app-daily-summary',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './daily-summary.component.html',
  styleUrl: './daily-summary.component.css',
})
export class DailySummaryComponent implements OnInit {
  summaries: WorkoutDailySummary[] = [];
  total = 0;
  loading = false;
  error: string | null = null;

  skip = 0;
  limit = 30;

  constructor(private workoutService: WorkoutService) {}

  ngOnInit(): void {
    this.loadSummaries();
  }

  loadSummaries(): void {
    this.loading = true;
    this.error = null;

  this.workoutService.getDailySummaries(this.skip, this.limit).subscribe({
    next: (data: PaginatedDailySummary) => {
      this.summaries = data.items;   // ← array for *ngFor    
      this.total = data.total;
      this.skip = data.skip;
      this.limit = data.limit;
      this.loading = false;
    },
    error: (err) => {
      this.error = err.message || 'Failed to load daily summaries';
      this.loading = false;
    },
  });
  }

  nextPage(): void {
    this.skip += this.limit;
    this.loadSummaries();
  }

  prevPage(): void {
    this.skip = Math.max(0, this.skip - this.limit);
    this.loadSummaries();
  }
}