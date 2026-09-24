import { Routes } from '@angular/router';
import { WorkoutFormComponent } from './components/workout-form/workout-form.component';

export const routes: Routes = [

  { path: 'workout', component: WorkoutFormComponent },
  // optional: redirect unknown paths
  { path: '**', redirectTo: '' }
];