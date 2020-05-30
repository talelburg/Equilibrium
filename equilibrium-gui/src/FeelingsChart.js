import React from "react";
import {Brush, CartesianGrid, Legend, Line, LineChart, Tooltip, XAxis, YAxis} from "recharts";
import moment from "moment";
import {Col, Container, Row} from "react-bootstrap";

class FeelingsChart extends React.Component {
    constructor(props) {
        super(props);
        this.state = {snapshots: [], feelings: []}
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}/snapshots`)
            .then(response => response.json())
            .then(data => this.setState({snapshots: data}))
            .then(() => this.state.snapshots.forEach(snapshot =>
                    fetch(`${window.api_server}/users/${this.props.user_id}/snapshots/${snapshot}/feelings`)
                        .then(response => response.json())
                        .then(data => this.setState({feelings: this.state.feelings.concat(data)}))
                )
            );
    }

    render() {
        return (
            <Container fluid>
                <Row>
                    <Col><h1>Feelings Over Time</h1></Col>
                </Row>
                <Row>
                    <Col><LineChart
                        width={1800}
                        height={650}
                        data={
                            this.state.feelings.map((feelings, idx) => {
                                return {
                                    date: moment(this.state.snapshots[idx]).format("DD/MM/YYYY HH:mm:ss:SSS"),
                                    hunger: feelings.hunger,
                                    thirst: feelings.thirst,
                                    exhaustion: feelings.exhaustion,
                                    happiness: feelings.happiness,
                                }
                            })
                        }
                        margin={{top: 5, right: 30, left: 20, bottom: 5}}
                    >
                        <CartesianGrid strokeDasharray="3 3"/>
                        <XAxis dataKey="date"/>
                        <YAxis/>
                        <Tooltip/>
                        <Legend/>
                        <Line type="monotone" dataKey="hunger" stroke="#FFFF00"/>
                        <Line type="monotone" dataKey="thirst" stroke="#FF00FF"/>
                        <Line type="monotone" dataKey="exhaustion" stroke="#00FFFF"/>
                        <Line type="monotone" dataKey="happiness" stroke="#000000"/>
                        <Brush/>
                    </LineChart></Col>
                </Row>
            </Container>
        );
    }
}

export default FeelingsChart;