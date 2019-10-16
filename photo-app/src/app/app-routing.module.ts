import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { UploadComponent } from './upload/upload.component';
import { LoadingComponent } from './loading/loading.component';
import { ResultComponent } from './result/result.component';

const routes: Routes = [
  { path: '', component: UploadComponent },
  { path: 'loading/:id', component: LoadingComponent },
  { path: 'result/:id', component: ResultComponent }
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
