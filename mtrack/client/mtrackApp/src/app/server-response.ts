export interface SignResult {
  signature: string;
  svg: string;
};

export interface VerifyResult {
  result: boolean;
  message: string;
};


export interface Hold {
  m_id: number
  name: string;
  pending:boolean;
};

export interface Pending {
  id: number;
  name: string;
  m_id: number;
};

export interface Transaction {
  id:number;
  medicine:string;
  buyer:string;
  seller:string;
  date:string;
  pending:boolean;
};

export interface ActionResult {
  result: boolean;
  data?:any;
};

