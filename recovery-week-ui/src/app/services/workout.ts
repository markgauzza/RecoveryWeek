import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

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
}