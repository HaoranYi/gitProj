use std::cell::RefCell;
use std::rc::Rc;

fn foo(v: &mut i32) {
    *v += 1;
}

struct S<T> {
    x: T,
    y: T,
}

//impl<T: std::ops::Add<Output = T> + Copy> S<T> {
impl<T> S<T>
where
    T: std::ops::Add<Output = T> + Copy,
{
    fn get_x(&self) -> T {
	self.x
    }
    fn get_y(&self) -> T {
	self.y
    }

    fn get_xy(&self) -> T {
	self.x + self.y
    }
}

fn main() {
    {
	// mut keyword: variable, reference, pointer
	let x: i32 = 5;
	let mut y: i32 = 5; // mut variable
	y = y + 1;
	let y_ref = &mut y; // mut ref
	*y_ref += 1;
	foo(y_ref);
	println!("{} {}", x, y);
    }

    {
	let x = 5i32;
	let mut y = 5i32;
	y = y + 1;
	println!("{} {}", x, y);
    }

    {
	println!("mut box");
	// immutable box
	let x = Box::new(5);
	println!("{}", x);

	// mutable box
	let mut y = Box::new(5); // mut pointer
	//let x = &y;  // ~~~ error!

	foo(&mut y);
	println!("{}", y);

	foo(&mut *y);
	println!("{}", y);

	*y = 7;
	println!("{}", y);
	//println!("{}", x); // ~~~error!
    }

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

    {
	for n in (1..4).rev() {
	    println!("{}", n);
	}
	let x = 5;
	match x {
	    1..=5 => println!("one through five"),
	    _ => println!("something else"),
	}

	if x == 5 {
	    println!("5");
	} else {
	    println!("not 5");
	}
    }

    {
	println!("struct");
	let x = S { x: 1, y: 2 };
	println!("{} {} {}", x.get_x(), x.get_y(), x.get_xy());
    }

    {
	println!("closure");
	let x = "hello";
	let foo = || {
	    println!("foo {}", x);
	};

	foo();
    }
    {
	println!("range");
	for i in 1..=5 {
	    print!("{} ", i);
	}
	println!("");
    }
}
