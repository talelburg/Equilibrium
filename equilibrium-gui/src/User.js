import React from "react";
import SnapshotCard from "./SnapshotCard";
import Snapshot from "./Snapshot";
import moment from "moment";
import FeelingsChart from "./FeelingsChart";
import {CardGroup, Nav, Navbar} from "react-bootstrap";

class User extends React.Component {
    constructor(props) {
        super(props);
        this.state = {snapshot: null, snapshots: [], display: null};
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}/snapshots`)
            .then(response => response.json())
            .then(data => this.setState({snapshots: data}))
    }

    selectSnapshot(timestamp) {
        this.setState({snapshot: timestamp, display: null})
    }

    selectDisplay(display) {
        this.setState({snapshot: null, display: display})
    }

    render() {
        let snapshots = this.state.snapshots;
        let data;
        if (this.state.snapshot == null) {
            switch (this.state.display) {
                case "feelings":
                    data = <FeelingsChart user_id={this.props.user_id}/>
                    break;
                case "snapshots":
                    data =
                        <CardGroup>
                            {snapshots.map((snapshot) =>
                                <SnapshotCard
                                    key={snapshot}
                                    user_id={this.props.user_id}
                                    timestamp={snapshot}
                                    onClick={() => this.selectSnapshot(snapshot)}
                                />
                            )}
                        </CardGroup>;
                    break;
                default:
                    data = <div/>
                    break;
            }
        } else {
            data = <Snapshot user_id={this.props.user_id} timestamp={this.state.snapshot}/>
        }
        return (
            <div className="user">
                <Navbar bg="primary" variant="dark" fixed="bottom">
                    <Nav variant="pills" className="mr-auto"
                         onSelect={eventKey => this.selectDisplay(eventKey)}>
                        <Nav.Item>
                            <Nav.Link eventKey="snapshots" variant="secondary">
                                All Snapshots
                            </Nav.Link>
                        </Nav.Item>
                        <Nav.Item>
                            <Nav.Link eventKey="feelings" variant="secondary">
                                Feelings Over Time
                            </Nav.Link>
                        </Nav.Item>
                    </Nav>
                    <Navbar.Collapse className="justify-content-end">
                        <Navbar.Text>
                            {this.state.snapshot == null ? "" : `Viewing snapshot from 
                            ${moment(this.state.snapshot).format("DD/MM/YYYY HH:mm:ss:SSS")}`}
                        </Navbar.Text>
                    </Navbar.Collapse>
                </Navbar>
                {data}
            </div>
        );
    }
}

export default User;