fn main() {
    let var1 = "test1";

    let ff = r#"{{"type": "type1", "type2": {}}}"#;

    let json = format!(r#"{{"type": "type1", "type2": {}}}"#, var1);
    //let json = format!(ff, var1);
    println!("{}", json);

    println!(
        r#"
        subgraph cluster_vote {{
        graph [style=dotted]
        label = vote;
        {}
        }}"#,
        "a->b",
    );

    println!(
        r#"
        subgraph cluster_lockout {{
        graph
        label = lockout;
        {}
        }}"#,
        "c->d"
    );
}
