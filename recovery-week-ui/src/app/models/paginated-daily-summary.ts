import { WorkoutDailySummary } from './workout-daily-summary';

export interface PaginatedDailySummary {
  total: number;
  skip: number;
  limit: number;
  items: WorkoutDailySummary[];
}
