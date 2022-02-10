enum Message {
    Hello { id: i32 },
}

fn main() {
    let msg = Message::Hello {id : 5 };
    match msg {
        Message::Hello {
            id: my_id @ 3..=7,
        } => println!("{}", my_id),
        Message::Hello {
            id: 10..=12,
        } => println!("no capture"),
        Message::Hello {
            id
        } => println!("default {}", id),
    }
}