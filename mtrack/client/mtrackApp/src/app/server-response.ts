export interface SignResult {
  signature: string;
  svg: string;
};

export interface VerifyResult {
  result: boolean;
  message: string;
};


export interface Hold {
  name: string;
};

export interface Pending {
  id: number;
  name: string;
};

export interface Transaction {
  id:number; 
  medicine_id:number;
  buyer_id:number;
  seller_id:number;
  created:string;
  last_update:string;
  state:number;
  parent_trans_id:number;
};

export interface ActionResult {
  result: boolean;
};

