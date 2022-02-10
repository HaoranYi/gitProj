// pattern to define user class

#[derive(Debug, Clone)]  // macro for compiler code gen
struct Session {         // define data fields in the class
    a: String,
    b: String,
}

impl Session {
    fn new(x: &str) -> Self {  // constructor
        Self {a: x.to_string(), b: x.to_string()}
    }

    fn hello(&self) {  // method
        println!("{} {}", self.a, self.b)
    }
}

fn main() {
    let s = Session::new("abc");
    s.hello();
}