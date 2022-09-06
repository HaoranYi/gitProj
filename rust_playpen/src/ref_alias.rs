// Rust Tip: use type alias with lifetime parameter
use std::marker::PhantomData;

type VecRef<'a, T> = &'a Vec<T>;

// struct with lifetime parameter associated with the type parameter
// this is how Iter<'a, T> are defined, which associate continer's lifetime with Iter through
// v.iter() method:
//     fn vec::iter(&self) -> Iter<'_, T>
// and then pass the lifetime (from the container) down to member fn returns, i.e. ref to the
// element
//     fn Iter::next(&self) -> Option<&'a T>
// To achieve this relay of lifetime parameter passing throught rust lifetime analyzer in the
// compiler, use PhantomData marker to enforce the lifetime restriction.
#[derive(Debug)]
pub struct Foo<'a, T: 'a> {
    _marker: PhantomData<&'a T>,
}

fn main() {
    //let v = vec![1, 2, 3];
    //let v: Vec<i32> = (1..5).collect();  // slice range to Vec
    let v = (1..5).collect::<Vec<i32>>(); // turbo fish syntax to specify types
    let r: VecRef<i32> = &v;

    println!("{:?}", v);
    println!("{:?}", r);

    // instantiation
    let f = Foo::<'static, i32> {
        _marker: PhantomData,
    };

    println!("{:?}", f);
}
