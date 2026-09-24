export interface WorkoutDailySummary {
  WorkoutDate: string;   // ISO date, e.g. "2026-09-22"
  Workouts: string;
  Sequence: number;
  DayOfWeek: string;
  DayParity: string;
}