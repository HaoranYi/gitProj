use std::collections::{BTreeMap, HashMap};

fn main() {
    let v = vec![1, 2, 3, 4];

    // by ref
    for x in &v {
        println!("AA {}", x);
    }

    // by copy
    for x in v.iter().copied() {
        println!("BB {}", x);
    }

    println!("{:?}", v);
}
