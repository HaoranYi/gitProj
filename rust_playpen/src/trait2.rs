trait A {
    fn a(&self) {
        println!("default impl");
    }
}

struct B {}

impl A for B {}

impl B {
    fn a(&self) {
        println!("override impl");
        A::a(self);
    }
}

fn main() {
    let a = B {};
    a.a();
}
