class ProductsList extends React.Component {
    constructor() {
        super();
        this.state = {
            ProductData: []
        }
    }

    componentDidMount() {
        axios.get("http://localhost:51260/api/products").then(response => {
            //console.log(response.data);
            this.setState({
                ProductData: response.data
            });
        });
    }

    render() {

        return (
            <section>
                <h1>Products List</h1>
                <div>
                    <table>
                        <thead><tr><th>Product Id</th><th>Product Name</th><th>Product Category</th><th>Product Price</th></tr></thead>
                        <tbody>
                            {
                                this.state.ProductData.map((p, index) => {
                                    return <tr key={index}><td>{p.ProductId}</td><td> {p.ProductName}</td><td>{p.ProductCategory}</td><td>{p.ProductPrice}</td></tr>;
                                })
                            }
                        </tbody>
                    </table>
                </div>


            </section>
        )
    }
}

ReactDOM.render(
    <ProductsList />,
    document.getElementById('myContainer'));
