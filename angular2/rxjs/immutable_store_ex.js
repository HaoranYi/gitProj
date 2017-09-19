import Immutable from 'immutable';
import someObservable from './someObservable';
import someObservable2 from './someObservable2';

var initialState = {
    foo: 'bar'
};

var state = Observable.merge(someObservable, someObservable2)
    .scan((state, changeFn)=>changeFn(state), Immutable.fromJS(initialState));

export default state

/////////////////// Usage /////////////////////////////////////////////////////
import state from './state'
state.subscribe(state => {
    document.querySelector('#text').innerHTML = state.get('foo');
});
