// Rust Tip: use type alias with lifetime parameter
type VecRef<'a, T> = &'a Vec<T>;

fn main() {
    //let v = vec![1, 2, 3];
    //let v: Vec<i32> = (1..5).collect();  // slice range to Vec
    let v = (1..5).collect::<Vec<i32>>(); // turbo fish syntax to specify types
    let r: VecRef<i32> = &v;

    println!("{:?}", v);
    println!("{:?}", r);
}
