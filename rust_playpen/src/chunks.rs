fn main()
{
    //let slice = ['l', 'o', 'r', 'e', 'm'];
    //let slice: Vec<char> = "lorem".chars().collect();
    let slice = String::from("lorem");
    let slice: Vec<char> = slice.chars().collect();
    let iter = slice.chunks(2);

    for x in iter {
        println!("{:?}", x);
    }
}
