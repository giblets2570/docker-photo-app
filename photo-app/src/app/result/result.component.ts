import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-result',
  templateUrl: './result.component.html',
  styleUrls: ['./result.component.scss']
})
export class ResultComponent implements OnInit {

  id: string = "";
  url: string = "";

  constructor(private route: ActivatedRoute, ) { }

  ngOnInit() {
    this.route.params.subscribe(params => {
       this.id = params['id']; // (+) converts string 'id' to a number
       // In a real app: dispatch action to load the details here.
       this.url = 'https://tomsstorage.blob.core.windows.net/tomscontainer/' + this.id;
    });
  }

}
