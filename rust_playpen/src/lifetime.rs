struct Foo<'a> {
    part: &'a str,
}

impl<'a> Foo<'a> {
    fn get(&self) -> &str {
        self.part
    }
}

// fn print_refs(x: &i32, y: &i32) // because of elision
fn print_refs<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("{} {}", x, y);
}

struct Owner(i32);

impl Owner {
    // can ommit lifetime because of elision
    fn add_one<'a>(&'a mut self) {
        self.0 += 1;
    }

    // can ommit lifetime because of elision
    fn print<'a>(&'a self) {
        println!("{}", self.0);
    }
}

fn main_owner() {
    let mut o = Owner(42);
    o.add_one();
    o.print();
}

#[derive(Debug)]
struct Borrowed<'a>(&'a i32);

#[derive(Debug)]
struct NamedBorrowed<'a> {
    x: &'a i32,
    y: &'a i32,
}

#[derive(Debug)]
enum Either<'a> {
    Num(i32),
    Ref(&'a i32),
}

fn main_structs() {
    let x = 18;
    let y = 15;

    let s = Borrowed(&x);
    let d = NamedBorrowed { x: &x, y: &y };
    let r = Either::Ref(&x);
    let num = Either::Num(y);

    println!("x is borrowed in {:?}", s);
    println!("x and y is borrowed in {:?}", d);
    println!("x is borrowed in {:?}", r);
    println!("y is not borrowed in {:?}", num);
}

const N: i32 = 10;
impl<'a> Default for Borrowed<'a> {
    fn default() -> Self {
        Self(&10) // const literal static lifetime
    }
}

fn main() {
    let s = String::from("haha hoho");
    let s0 = s.split(' ').next().expect("ok");
    let r; // = &String::from("abc")[..];
    {
        let f = Foo { part: s0 };
        r = f.get();
    }

    // failed to compile because of rust compiler don't know that the ref is to s
    // not for foo. not seeing one more level of ref.
    //println!("{}", r);
    //
    main_owner();

    main_structs();
}
