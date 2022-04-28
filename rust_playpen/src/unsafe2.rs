/// This file illustrate how to abuse rust lifetime with unsafe code and raw poiner. It is like a
/// nuclear weapon.  Normally you don't need it. But for some case, it might be handy to work
/// around rust lifetime checker.
use std::ptr;

#[derive(Debug)]
struct Point {
    x: u8,
    y: u8,
}

fn foo() -> *const Point {
    let p = Point { x: 1, y: 2 };
    print!("{:?}\n", p);
    &p as *const _
}

fn main() {
    let mut p1: *const Point = ptr::null();
    {
        let p = Point { x: 1, y: 2 };
        print!("{:?}\n", p);
        p1 = &p as *const _;
    }

    // access local scope struct
    let p2 = unsafe { p1.as_ref() };
    print!("{:?}\n", p2);

    // access local struct from foo function!!!
    p1 = foo();
    let p2 = unsafe { p1.as_ref() };
    print!("{:?}\n", p2);
}
