import messages from './someObservable';

class MyComponent extens ObservableComponent {
    constructor(props) {
        super(props);
        this.state = { messages: [] };
    }
    componentDidMount() {
        this.messages = messages.scan((messages, message) => [message].concat(messages), [])
            .subscribe(messages => this.setState({messages:messages}));

    }
    componentWillUnmount() {
        this.messages.unsubscribe();
    }
    render() {
        return(
        <div>
            <ul>
                {this.state.messages.map(message => <li>{message.text}</li>)}
            </ul>
        </div>
        );
    }
}

export default MyComponent;
