import { Component, OnInit } from '@angular/core';
import { DomSanitizer, SafeUrl } from '@angular/platform-browser';
import { Router } from '@angular/router';
import { FileUploader, FileSelectDirective, FileItem } from 'ng2-file-upload/ng2-file-upload';

const URL = 'http://localhost:4000/api/upload';

@Component({
  selector: 'app-upload',
  templateUrl: './upload.component.html',
  styleUrls: ['./upload.component.scss']
})
export class UploadComponent implements OnInit {

  public uploader: FileUploader = new FileUploader({ url: URL, itemAlias: 'photo' });
  public filePreviewPath: SafeUrl;

  constructor(private sanitizer: DomSanitizer, private router: Router) {
    this.uploader.onAfterAddingFile = (fileItem) => {
      this.filePreviewPath  = this.sanitizer.bypassSecurityTrustUrl((window.URL.createObjectURL(fileItem._file)));
    }
    this.uploader.onCompleteItem = (item, response, status, headers) => {
      this.router.navigate([`/loading/${JSON.parse(response).filename}`]);
    }
  }

  upload() {
    let items = this.uploader.getNotUploadedItems().filter((item: FileItem) => !item.isUploading);
    if (!items.length) {
      return;
    }
    console.log(items)
    this.uploader.uploadAll();
  }

  ngOnInit() {

  }

}
