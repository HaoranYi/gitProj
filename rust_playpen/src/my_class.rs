// pattern to define your own user class

use std::ops::Range;

#[derive(Debug, Clone)]  // macro for compiler code gen
struct Session {         // define data fields in the class
    a: String,
    b: String,
}

impl Session {
    // constructor
    fn new(x: &str) -> Self {
        Self {a: x.to_string(), b: x.to_string()}
    }

    // another constructor returns Option<T>
    fn new_from(x: i32) -> Option<Self> {
        Some(Self {a: x.to_string(), b: (x+1).to_string()})
    }

    // method
    fn hello(&self) {
        println!("{} {}", self.a, self.b);
    }

    // another method
    fn bar(&self) {
        println!("another method bar");
    }

    // no infer for return type
    fn gen_range(&self) -> Range<i32> {
        1..10
    }
}

fn main() {
    let s = Session::new("abc");
    s.hello();
    s.bar();

    let s = Session::new_from(1).unwrap();
    s.hello();
    s.bar();

    println!("{:?}", s.gen_range());
}