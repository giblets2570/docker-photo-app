import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { interval, Observable } from 'rxjs';
import { Router } from '@angular/router';

// Create an Observable that will publish a value on an interval
const URL = 'http://localhost:4000/api/conversion';

const wait = (n) => new Promise((resolve) => setTimeout(resolve, n * 1000));

@Component({
  selector: 'app-loading',
  templateUrl: './loading.component.html',
  styleUrls: ['./loading.component.scss']
})
export class LoadingComponent implements OnInit {

  // secondsCounter: Observable = interval(2000);
  id: string = "";

  constructor(private route: ActivatedRoute, private router: Router) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
       this.id = params['id'];
    });
    this.check();
  }

  async check() {
    let response = await fetch(URL + '?filename=' + this.id);
    let json = await response.json();
    if (json.filename && json.filename !== 'Loading') {
      this.router.navigate([`/result/${json.filename}`]);
    } else {
      await wait(2);
      this.check();
    }
  }

}
