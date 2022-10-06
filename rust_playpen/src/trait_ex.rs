/// example of traits composition (dependency injection)

trait Speaks {
    fn speak(&self);
}

trait Animal {
    fn kind(&self) -> &str;
    fn noise(&self) -> &str;
}

impl<T: Animal> Speaks for T
//where
//    T: Animal,
{
    fn speak(&self) {
        println!("the {} said {},", self.kind(), self.noise());
    }
}

struct Cat {}
struct Dog {}

impl Animal for Cat {
    fn kind(&self) -> &str {
        "cat"
    }
    fn noise(&self) -> &str {
        "meow"
    }
}

impl Animal for Dog {
    fn kind(&self) -> &str {
        "dog"
    }
    fn noise(&self) -> &str {
        "woof"
    }
}

trait Human {
    fn name(&self) -> &str;
    fn words(&self) -> &str;
}

// not workd because  conflicting implementations of trait `Speaks`
impl<T: Human> Speaks for T
//where
//    T: Human,
{
    fn speak(&self) {
        println!("the {} said {},", self.name(), self.words());
    }
}

struct Person {}
impl Human for Person {
    fn name(&self) -> &str {
        "human"
    }
    fn words(&self) -> &str {
        "blabla"
    }
}

pub fn main() {
    let dog = Dog {};
    let cat = Cat {};
    dog.speak();
    cat.speak();

    let p = Person {};
    p.speak();
}
