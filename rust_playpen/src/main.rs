//use rand::prelude::*;

fn print_refs<'a, 'b>(x: &'a i32, y: &'b i32) {
    println!("x is {} and y is {}", x, y);
}

// A function which takes no arguments, but has a lifetime parameter `'a`.
fn failed_borrow<'a>() {
    let _x = 12;

    // ERROR: `_x` does not live long enough
    let _y: &i32 = &_x;
    // Attempting to use the lifetime `'a` as an explicit type annotation
    // inside the function will fail because the lifetime of `&_x` is shorter
    // than that of `y`. A short lifetime cannot be coerced into a longer one.
}

fn t1() {
    // Create variables to be borrowed below.
    let (four, nine) = (4, 9);

    // Borrows (`&`) of both variables are passed into the function.
    print_refs(&four, &nine);
    // Any input which is borrowed must outlive the borrower.
    // In other words, the lifetime of `four` and `nine` must
    // be longer than that of `print_refs`.

    failed_borrow();
    // `failed_borrow` contains no references to force `'a` to be
    // longer than the lifetime of the function, but `'a` is longer.
    // Because the lifetime is never constrained, it defaults to `'static`.
}

struct Owner(i32);

impl Owner {
    // Annotate lifetimes as in a standalone function.
    fn add_one<'a>(&'a mut self) {
        self.0 += 1;
    }
    fn print<'a>(&'a self) {
        println!("`print`: {}", self.0);
    }
}

fn t2() {
    let mut owner = Owner(18);

    owner.add_one();
    owner.print();
}

const fn const_add(x: i32, y: i32) -> i32 {
    //x + y +  rand::random::<i32>()
    x + y
}

// A type `Borrowed` which houses a reference to an
// `i32`. The reference to `i32` must outlive `Borrowed`.
#[derive(Debug)]
struct Borrowed<'a>(&'a i32);

// Similarly, both references here must outlive this structure.
#[derive(Debug)]
struct NamedBorrowed<'a> {
    x: &'a i32,
    y: &'a i32,
}

// An enum which is either an `i32` or a reference to one.
#[derive(Debug)]
enum Either<'a> {
    Num(i32),
    Ref(&'a i32),
}

fn t3() {
    let x = 18;
    let y = 15;

    let single = Borrowed(&x);
    let double = NamedBorrowed { x: &x, y: &y };
    let reference = Either::Ref(&x);
    let number = Either::Num(y);

    println!("x is borrowed in {:?}", single);
    println!("x and y are borrowed in {:?}", double);
    println!("x is borrowed in {:?}", reference);
    println!("y is *not* borrowed in {:?}", number);
}

fn t4() {
    let s1 = String::from("hello");

    let len = calculate_length(&s1);

    println!("The length of '{}' is {}.", s1, len);
}

fn calculate_length<'a>(s: &'a String) -> usize {
    s.len()
}

fn t5() {
    let x = 5;
    let y = &x;

    assert_eq!(5, x);
    assert_eq!(5, *y);
}

fn main() {
    t1();
    t2();
    t3();
    t4();
    t5();

    // Iterators can be collected into vectors
    let mut collected_iterator: Vec<i32> = (0..10).collect();
    println!("Collected (0..10) into: {:?}", collected_iterator);

    // The `vec!` macro can be used to initialize a vector
    let mut xs = vec![1i32, 2, 3];
    println!("Initial vector: {:?}", xs);

    // Insert new element at the end of the vector
    println!("Push 4 into the vector");
    xs.push(4);
    println!("Vector: {:?}", xs);

    // Error! Immutable vectors can't grow
    collected_iterator.push(0);
    println!("{:?}", collected_iterator);
    // FIXME ^ Comment out this line

    // The `len` method yields the number of elements currently stored in a vector
    println!("Vector length: {}", xs.len());

    // Indexing is done using the square brackets (indexing starts at 0)
    println!("Second element: {}", xs[1]);

    // `pop` removes the last element from the vector and returns it
    println!("Pop last element: {:?}", xs.pop());

    // Out of bounds indexing yields a panic
    //println!("Fourth element: {}", xs[3]);
    // FIXME ^ Comment out this line

    // `Vector`s can be easily iterated over
    println!("Contents of xs:");
    for x in xs.iter() {
        println!("> {}", x);
    }

    // A `Vector` can also be iterated over while the iteration
    // count is enumerated in a separate variable (`i`)
    for (i, x) in xs.iter().enumerate() {
        println!("In position {} we have value {}", i, x);
    }

    // Thanks to `iter_mut`, mutable `Vector`s can also be iterated
    // over in a way that allows modifying each value
    for x in xs.iter_mut() {
        *x *= 3;
    }
    println!("Updated vector: {:?}", xs);

    {
        let x = Box::new(5);
        let y = &x;
        println!("{} {}", x, y);
    }

    {
        let x = 5;
        let y = &x;
        println!("haha {:?} {:p}", x, y);
    }

    {
        let x = vec![1, 2, 3];

        let equal_to_x = move |z| z == x;

        //println!("can't use x here: {:?}", x);

        let y = vec![1, 2, 3];

        assert!(equal_to_x(y));

        {
            //let x = 1i32;
            let x = rand::random::<i32>();

            //let mut input = String::new();
            //std::io::stdin().read_line(&mut input).unwrap();
            //let x: i32 = input.trim().parse().unwrap();
            let y = 1i32;
            let z = const_add(x, y);
            println!("const_add: {}", z);
        }

        {
            let sum = 100;
            let v: Vec<i32> = (1..100).collect();

            fn find_pairs(v: &Vec<i32>, sum: i32) -> i32 {
                let mut n: i32 = 0;
                for i in 0..v.len() {
                    for j in i + 1..v.len() {
                        if v[i] + v[j] == sum {
                            n += 1;
                        }
                    }
                }
                return n;
            }

            println!("{}", find_pairs(&v, sum));

            // range
            for i in (1..20).step_by(2) {
                println!("step: {}", i);
            }
        }

        {
            // tuple
            let my_tuple = ("hello", 5, 'c');
            println!("tuple: {} {} {}", my_tuple.0, my_tuple.1, my_tuple.2);
        }

        {
            // array
            //let my_arr = &[1, 2, 3];
            let my_arr = &[1; 3];
            // std::fmt, akin to python string.format or C printf
            println!("arr: {:?}", my_arr);
        }
        {
            let x = 3;
            if x == 3 {
                println!("three");
            } else {
                println!("not three");
            }
        }
        println!("done");
    }
}

#[cfg(test)]
mod tests {
    #[test]
    fn foo() {
        assert_eq!(2 + 2, 4);
    }
}
