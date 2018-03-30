import { Component, OnInit, OnDestroy } from '@angular/core';
import { ActivatedRoute } from "@angular/router";
import { VendorService } from '../vendor.service';

@Component({
  selector: 'app-sell',
  templateUrl: './sell.component.html',
  styleUrls: ['./sell.component.css']
})
export class SellComponent implements OnInit, OnDestroy {
  vendor: string;
  id: number;
  name: string;
  private sub: any;

  constructor(private route: ActivatedRoute, private vendorSvc: VendorService) { }

  ngOnInit() {
    this.sub = this.route.params.subscribe(params => {
      this.id = +params['id']; 
      this.name = params['name'];
    });
    this.vendorSvc.currentVendor.subscribe(vendor=> this.vendor= vendor);
  }

  ngOnDestroy() {
    this.sub.unsubscribe();
  }
}
