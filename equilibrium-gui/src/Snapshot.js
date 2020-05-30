import React from "react";
import {Accordion, Button, Card, ListGroup} from "react-bootstrap";
import {PolarAngleAxis, PolarGrid, PolarRadiusAxis, Radar, RadarChart} from "recharts";


class Snapshot extends React.Component {
    constructor(props) {
        super(props);
        this.state = {feelings: null, pose: null, color_image: null, depth_image: null};
    }

    componentDidMount() {
        fetch(`${window.api_server}/users/${this.props.user_id}/snapshots/${this.props.timestamp}`)
            .then(response => response.json())
            .then(data => data.results.forEach(result =>
                fetch(`${window.api_server}/users/${this.props.user_id}/snapshots/${this.props.timestamp}/${result}`)
                    .then(response => response.json())
                    .then(data => {
                        if (!data.hasOwnProperty("data")) {
                            this.setState({[result]: data})
                        }
                        else {
                            fetch(`${window.api_server}/${data.data}`)
                                .then(response => response.json())
                                .then(data => this.setState({[result]: data}))
                        }
                    })
            ));
    }

    render() {
        if (this.state.feelings == null || this.state.pose == null
            || this.state.color_image == null || this.state.depth_image == null) {
            return <div/>;
        }
        let feelings = this.state.feelings
        let translation = this.state.pose.translation;
        let rotation = this.state.pose.rotation;
        return (
            <Accordion>
                <Card className="text-center" bg="dark" text="white">
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="feelings">
                            Feelings
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="feelings">
                        <Card.Body>
                            <RadarChart cx={300} cy={250} outerRadius={150} width={500} height={500}
                                        data={[
                                            {name: "Hunger", value: feelings.hunger},
                                            {name: "Thirst", value: feelings.thirst},
                                            {name: "Exhaustion", value: feelings.exhaustion},
                                            {name: "Happiness", value: feelings.happiness},

                                        ]}
                            >
                                <PolarGrid/>
                                <PolarAngleAxis dataKey="name"/>
                                <PolarRadiusAxis angle={30} domain={[-1, 1]}/>
                                <Radar name="Feelings" dataKey="value" stroke="#8884d8" fill="#8884d8"
                                       fillOpacity={0.6}/>
                            </RadarChart>
                        </Card.Body>
                    </Accordion.Collapse>
                </Card>
                <Card className="text-center" bg="dark" text="white">
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="pose">
                            Pose
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="pose">
                        <ListGroup variant="flush">
                            <ListGroup.Item variant="dark">
                                Translation: ({translation.x}, {translation.y}, {translation.z})
                            </ListGroup.Item>
                            <ListGroup.Item variant="dark">
                                Rotation: ({rotation.x}, {rotation.y}, {rotation.z}, {rotation.w})
                            </ListGroup.Item>
                        </ListGroup>
                    </Accordion.Collapse>
                </Card>
                <Card className="text-center" bg="dark" text="white">
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="color_image">
                            Color Image
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="color_image">
                        <img src={`data:image/jpeg;base64,${this.state.color_image.data}`}  alt=""/>
                    </Accordion.Collapse>
                </Card>
                <Card className="text-center" bg="dark" text="white">
                    <Card.Header>
                        <Accordion.Toggle as={Button} variant="link" eventKey="depth_image">
                            Depth Image
                        </Accordion.Toggle>
                    </Card.Header>
                    <Accordion.Collapse eventKey="depth_image">
                        <img src={`data:image/jpeg;base64,${this.state.depth_image.data}`} alt="" />
                    </Accordion.Collapse>
                </Card>
            </Accordion>
        );
    }
}

export default Snapshot;