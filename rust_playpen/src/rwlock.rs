use std::collections::HashMap;
use std::sync::Arc;
use std::sync::RwLock;
use std::thread;

fn main() {
    let l = Arc::new(RwLock::new(Vec::<i32>::new()));

    let mut ths = vec![];

    for i in 1..10 {
        let l = Arc::clone(&l);
        ths.push(thread::spawn(move || loop {
            for k in 1..10 {
                l.write().unwrap().push(k);
                println!("{} {}", i, k);
            }

            l.write().unwrap().clear();
        }));
    }

    for h in ths {
        h.join().unwrap();
    }
}
