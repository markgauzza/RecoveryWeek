import { Component, EventEmitter, OnInit, Output, ChangeDetectorRef, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkoutService } from '../../services/workout';
import { WorkoutType } from '../../models/workout-type';
import { finalize } from 'rxjs/operators';

@Component({
  selector: 'app-workout-form',
  standalone: true,
  imports: [CommonModule, FormsModule],
  templateUrl: './workout-form.component.html',
  styleUrl: './workout-form.component.css',
})
export class WorkoutFormComponent implements OnInit {
  @Output() saved = new EventEmitter<void>();
  @Output() cancelled = new EventEmitter<void>();

  private cdr = inject(ChangeDetectorRef);

  workoutTypes: WorkoutType[] = [];
  loadingTypes = false;
  saving = false;
  error: string | null = null;

  selectedTypeId: number | null = null;
  workoutDate: string = this.today();
  hours = 0;
  minutes = 0;
  sequence: number | null = null;

  constructor(private workoutService: WorkoutService) {}

  ngOnInit(): void {
    debugger;
    this.loadWorkoutTypes();
  }

  today(): string {
    return new Date().toISOString().slice(0, 10);
  }

 loadWorkoutTypes(): void {
    this.loadingTypes = true;
    this.error = null;
    this.cdr.detectChanges();

    this.workoutService.getWorkoutTypes()
      .pipe(
        finalize(() => {
          this.loadingTypes = false;
          this.cdr.detectChanges();
        })
      )
      .subscribe({
        next: (types) => {
          console.log('workout types', types);
          this.workoutTypes = types ?? [];
          this.cdr.detectChanges();
        },
        error: (err) => {
          console.error('workout types error', err);
          this.error = 'Failed to load workout types';
          this.workoutTypes = [];
          this.cdr.detectChanges();
        },
      });
  }

  toSeconds(): number {
    const h = Math.min(60, Math.max(0, Number(this.hours) || 0));
    const m = Math.min(60, Math.max(0, Number(this.minutes) || 0));
    return h * 3600 + m * 60;
  }

  submit(): void {
    this.error = null;

    if (this.selectedTypeId == null) {
      this.error = 'Workout type is required';
      return;
    }
    if (!this.workoutDate) {
      this.error = 'Workout date is required';
      return;
    }
    if (this.sequence == null || this.sequence < 1 || this.sequence > 6) {
      this.error = 'Sequence must be between 1 and 6';
      return;
    }

    const body = {
      WorkoutTypeId: this.selectedTypeId,
      WorkoutDate: new Date(this.workoutDate + 'T12:00:00').toISOString(),
      TotalSeconds: this.toSeconds(),
      Sequence: this.sequence,
    };

    this.saving = true;
    this.workoutService.createWorkout(body).subscribe({
      next: () => {
        this.saving = false;
        this.saved.emit();
      },
      error: (err) => {
        this.saving = false;
        this.error =
          err.error?.detail?.message ||
          err.error?.detail ||
          err.message ||
          'Failed to create workout';
      },
    });
  }

  cancel(): void {
    this.cancelled.emit();
  }
}