use std::collections::{HashMap, BTreeMap};

fn main()
{
    let v = vec![1,2,3,4];
    println!("{:?}", v);

    let mut m = HashMap::new();
    m.insert("a", 1);
    m.insert("b", 2);
    println!("{:?}", m);

    let mut m2 = BTreeMap::new();
    m2.insert("a", 1);
    m2.insert("b", 1);
    m2.insert("c", 1);
    m2.insert("d", 1);
    println!("{:?}", m2);
}