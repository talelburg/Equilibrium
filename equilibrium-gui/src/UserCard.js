import React from "react";
import {Button, Card} from "react-bootstrap";

class UserCard extends React.Component {
    constructor(props) {
        super(props);
        this.state = {data: {}};
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}`)
            .then(response => response.json())
            .then(data => this.setState({data: data})
            );
    }

    render() {
        let data = this.state.data;
        return (
            <div>
                <Card className="text-center" bg="dark" text="white">
                    <Card.Body>
                        <Card.Title>{data.username}</Card.Title>
                        <Card.Subtitle>#{data.user_id}</Card.Subtitle>
                        <Card.Text>
                            {data.gender === 0 ? 'Male' : data.gender === 1 ? "Female" : "Other"},
                            born {new Date(data.birthday * 1000).toDateString()}
                        </Card.Text>
                        <Button variant="link" onClick={this.props.onClick}>Snapshots</Button>
                    </Card.Body>
                </Card>
            </div>
        );
    }
}

export default UserCard;