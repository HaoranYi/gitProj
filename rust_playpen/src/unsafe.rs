fn main() {
    let mut a = 3;
    // create raw pointer in safe code.
    // The following code is not valid when using reference, two refs read and write can't be
    // borrowed together.
    let b = &mut a as *mut _;
    let b2 = &a as *const _;
    // raw pointer can only be deferenced in unsafe code
    unsafe {
      *b += 1;
      *b.offset(100) += 1;
      println!("{}", *b2);
    }
    println!("{}", a);

    // convert raw pointer to an Option<&T>, which can then be used in safe code
    let c = unsafe {b.as_ref()};
    println!("{:?}", c);
}
