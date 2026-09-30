import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { WorkoutDayOfWeekReportRow } from '../models/workout-day-of-week-report';

@Injectable({
  providedIn: 'root'
})
export class ReportsService {
  constructor(private http: HttpClient) {}

  getWorkoutsByDayOfWeek(): Observable<WorkoutDayOfWeekReportRow[]> {
    return this.http.get<WorkoutDayOfWeekReportRow[]>(
      'http://localhost:8000/api/reports/workouts-by-day-of-week'
    );
  }
}