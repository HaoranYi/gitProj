import { Injectable } from '@angular/core';
import { BehaviorSubject } from 'rxjs/BehaviorSubject';



@Injectable()
export class MessageService {
  private messageSource = new BehaviorSubject<string>("");
  public currentMessage = this.vendorSource.asObservable();

  constructor() { }

  addMessage(msg: string) {
    this.messageSource.next(msg)
  }

}
