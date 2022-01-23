/// leetcode 2138: divide a string into group of size K

fn divide_string(s: &str, n: usize, fill: char) {
    for x in s.chars().collect::<Vec<char>>().chunks(n) {
	if x.len() == n {
	    println!("{}", x.iter().collect::<String>());
	}
	else {
	    let r = x.iter().collect::<String>();
	    println!("{}{}", r, fill.to_string().repeat(n - x.len()));
	}
    }
}


fn divide_string2(s: &str, n: usize, fill: char) {
    // str slice can't chunk because each char is not fixed size. transform it into bytes slice first.
    for x in s.as_bytes().chunks(n) {
	if x.len() == n {
	    println!("{}", String::from_utf8_lossy(x))
	}
	else {
	    println!("{}{}", String::from_utf8_lossy(x), fill.to_string().repeat(n - x.len()));
	}
    }
}


fn main() {
    let s = "abcdefg";
    divide_string2(&s, 2, 'x')
}
