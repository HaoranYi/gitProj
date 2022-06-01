struct Foo<'a> {
    part: &'a str,
}

impl<'a> Foo<'a> {
    fn get(&self) -> &str {
        self.part
    }
}

fn main() {
    let s = String::from("haha hoho");
    let s0 = s.split(' ').next().expect("ok");
    let r; // = &String::from("abc")[..];
    {
        let f = Foo { part: s0 };
        r = f.get(); // failed to compile because of rust compiler don't know that the ref is to s
                     // not for foo. not seeing one more level of ref.
    }
    println!("{}", r);
}
