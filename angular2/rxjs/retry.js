const source = Rx.Observable.interval(1000);
const example = source.flatMap(val=>{
    // throw error for demonstration
    if (val>5) {
        return Rx.Observable.throw('Error!');
    }
    return Rx.Observable.of(val);
}).retry(2);

const subscribe = example.subscribe({
    next: val=>console.log(val),
    error: val=>console.log(`${val}: retries 2 times then quit!`)
});


// retry-when
const source = Rx.Observable.interval(1000);
const example = source.flatMap(val=>{
    // throw error for demonstration
    if (val>5) {
        return Rx.Observable.throw('Error!');
    }
    return Rx.Observable.of(val);
}).retryWhen(error=>erros
                .do(val=>console.log(`Value ${val} was too high!`))
                .delayWhen(val=>Rx.Observable.timer(val*1000))
            );

const subscribe = example.subscribe(val=>console.log(val));
