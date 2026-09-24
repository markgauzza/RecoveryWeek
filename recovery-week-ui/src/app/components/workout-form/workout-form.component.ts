import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { WorkoutService, WorkoutType } from '../../services/workout';

@Component({
  selector: 'app-workout-form',
  standalone: true,                    // remove if you're still using NgModules
  imports: [CommonModule, FormsModule],
  templateUrl: './workout-form.component.html'
  
})
export class WorkoutFormComponent implements OnInit {
  workoutTypes: WorkoutType[] = [];
  selectedTypeId: number | null = null;
  loading = true;
  error: string | null = null;

  constructor(private workoutService: WorkoutService) {}

  ngOnInit(): void {
    this.loadWorkoutTypes();
  }

  loadWorkoutTypes(): void {
    this.workoutService.getWorkoutTypes().subscribe({
      next: (data) => {
        this.workoutTypes = data;
        this.loading = false;
      },
      error: (err) => {
        console.error(err);
        this.error = 'Failed to load workout types';
        this.loading = false;
      }
    });
  }
}