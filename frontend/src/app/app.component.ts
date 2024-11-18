import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { FormControl, ReactiveFormsModule } from '@angular/forms';
import { NgxAudioWaveModule } from 'ngx-audio-wave';
import { MatProgressBarModule } from '@angular/material/progress-bar';
import { NgClass } from '@angular/common';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, ReactiveFormsModule, NgxAudioWaveModule, 
    MatProgressBarModule, NgClass],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'AITourGuide';
  audio = '';
  audioUrl = '';
  imgUrl = '';
  ready = true;
  url = new FormControl('url')
  guides = [
    "Brian", 
    "Ava", 
    "Guy"
  ]
  guide = this.guides[0]
  invalid = false;

  constructor() {
    this.url.setValue('')
  }

  select(id: number) {
    this.guide = this.guides[id];
  }

  async submit() {
    this.ready = false;
    const body = {
      "url": this.url.getRawValue(),
      "guide": this.guide
    }
    this.url.setValue('');
    this.audio = '';
    this.audioUrl = '';
    this.imgUrl = '';
    body.url = body.url || '';
    const img = await (await fetch(body.url)).blob()
    if (img.type.startsWith('image')) {
      this.imgUrl = URL.createObjectURL(img);
      this.invalid = false;
      let resp = await fetch('http://localhost:3000', {
        method: 'POST',
        body: JSON.stringify(body),
      });
      this.audio = URL.createObjectURL(await resp.blob());
      this.audioUrl = body.url;
    } else {
      this.invalid = true;
    }
    this.ready = true;
  }

  resetValid() {
    this.invalid = false;
  }
}
