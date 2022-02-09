/// Option and Result

fn test_result_type() {
    println!("test Result:");
    let r: Result<i32, &str> = Ok(1);
    assert!(r.is_ok());
    assert!(!r.is_err());

    // map: takes fn, which works on inner type and return inner type, which then wrapped into Ok
    let r1: Result<&str, &str> = r.map(|_i| "number");
    println!("{:?}", r1);

    // and_then: takes fn, which works on inner type but return a Result (no wrapping)
    let r2: Result<_, _> = r.and_then(|i| Ok(i*i));
    println!("{:?}", r2);

    let i = r.unwrap();
    println!("{}", i);
}

fn test_option_type() {
    println!("test Option:");
    let o: Option<i32> = Some(2);
    assert!(o.is_some());
    assert!(!o.is_none());

    // map: takes fn, which works on the inner type and return inner type, which will be wrapped into Some
    let o1 = o.map(|_x| "some");
    println!("{:?}", o1);

    // and_then: takes fn, which works on the inner type and return Option type (no wrapping)
    let o2 = o.and_then(|_x| Some("some2"));
    println!("{:?}", o2);

    let i = o.unwrap();
    println!("{}", i);
}

fn main() {
    test_result_type();
    test_option_type();
}