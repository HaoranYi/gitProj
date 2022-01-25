use std::rc::Rc;
use std::cell::RefCell;

fn main() {
    // immutable box
    let x = Box::new(5);
    println!("{}", x);

    // mutable box
    let mut y = Box::new(5);
    *y = 7;
    println!("{}", y);

    {
	// share with ref count (immutable)
	let z1 = Rc::new(1);
	let z2 = Rc::clone(&z1);
	let z3 = Rc::clone(&z2);
	println!("{} {} {}", z1, z2, z3);
    }

    {
	// single owner but can be borrow_mut
	let z1 = RefCell::new(2);
	println!("{}", z1.borrow());
	*z1.borrow_mut() = 3;
	println!("{}", z1.borrow());
    }

    {
	// compose Rc and RefCell to make it share and mutable
	let z1 = Rc::new(RefCell::new(5));
	let z2 = Rc::clone(&z1);
	println!("{} {}", z1.borrow(), z2.borrow());
	*z2.borrow_mut() = 6;
	println!("{} {}", z1.borrow(), z2.borrow());
    }
}
