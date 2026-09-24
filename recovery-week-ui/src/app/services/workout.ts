import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { PaginatedDailySummary } from '../models/paginated-daily-summary';
export interface WorkoutType {
  WorkoutTypeId: number;
  WorkoutName: string;
  // add any other fields your API returns
}

@Injectable({
  providedIn: 'root'
})
export class WorkoutService {
  private apiUrl = 'http://localhost:8000/api';   // change if your API is on a different host/port

  constructor(private http: HttpClient) {}

  getWorkoutTypes(): Observable<WorkoutType[]> {
    return this.http.get<WorkoutType[]>(`${this.apiUrl}/workouts/types`);
  }

getDailySummaries(skip = 0, limit = 30): Observable<PaginatedDailySummary> {
  const params = new HttpParams()
    .set('skip', skip)
    .set('limit', limit);

  return this.http.get<PaginatedDailySummary>(
    `${this.apiUrl}/workouts/daily-summary`,
    { params }
  );
}
} 
