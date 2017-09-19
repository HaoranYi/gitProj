var increaseButton = document.querySelector('#increase');
var increase = Rx.Observable.fromEvent(increaseButton, 'click')
    .map(() => state => Object.assing({}, state, {count: state.count+1}));

var decreaseButton = document.querySelector('#decrease');
var decrease = Rx.Observable.fromEvent(decreaseButton, 'click')
    .map(() => state => Object.assing({}, state, {count: state.count-1}));

var inputElement = document.querySelector('#input');
var input = Rx.Observable.fromEvent(inputElement, 'keypress')
    .map(event => state => Object.assing({}, state, {inputValue: event.target.value}));

var state = Rx.Observable.merge(increase, decrease, input)
    .scan((state, changeFn) => changeFn(state), {
            count: 0,
            inputValue: ''
        });
state.subscribe((state) => {
    document.querySelector('#count').innerHTML = state.count;
    document.querySelector('#hello').innerHTML = 'Hello ' + state.inputValue;
});

var prevState = {};
state.subscribe((state) => {
    if (state.count !== prevState.count)
        document.querySelector('#count').innerHTML = state.count;

    if (state.inputValue !== prevState.inputValue)
        document.querySelector('#hello').innerHTML = 'Hello ' + state.inputValue;
    prevState = state;
});
