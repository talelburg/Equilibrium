import React from "react";
import moment from "moment";
import {Button, Card} from "react-bootstrap";

class SnapshotCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {data: {}}
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}/snapshots/${this.props.timestamp}`)
            .then(response => response.json())
            .then(data => this.setState({data: data})
            );
    }

    render() {
        let data = this.state.data;
        return (
            <div>
                <Card className="text-center" bg="dark" text="white" style={{}}>
                    <Card.Body>
                        <Button variant="link" onClick={this.props.onClick}>
                            {moment(data.timestamp).format("DD/MM/YYYY HH:mm:ss:SSS")}
                        </Button>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default SnapshotCard;