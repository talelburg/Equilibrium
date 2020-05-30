import React from 'react';
import CardDeck from 'react-bootstrap/CardDeck';
import logo from './logo.svg';
import './App.css';
import UserCard from "./UserCard";
import Navbar from "react-bootstrap/Navbar";
import Nav from "react-bootstrap/Nav";
import NavDropdown from "react-bootstrap/NavDropdown";
import User from "./User";

class App extends React.Component {
    constructor(props) {
        super(props);
        this.state = {user: null, users: []};
    }

    componentDidMount() {
        fetch(`${window.api_server}/users`)
            .then(response => response.json())
            .then(data => this.setState({users: data})
            );
    }

    selectUser(userId) {
        this.setState({user: userId});
    }

    render() {
        let users = this.state.users;
        let data;
        if (this.state.user == null) {
            data =
                <CardDeck>
                    {users.map((user) =>
                        <UserCard
                            key={user.user_id}
                            user_id={user.user_id}
                            onClick={() => this.selectUser(user.user_id)}
                        />
                    )}
                </CardDeck>;
        } else {
            data =
                <User user_id={this.state.user}/>
        }
        return (
            <div className="App">
                <Navbar bg="primary" variant="dark">
                    <Navbar.Brand>
                        <img
                            alt=""
                            src={logo}
                            width="30"
                            height="30"
                            className="d-inline-block align-top"
                        />
                        {" "}Equilibrium
                    </Navbar.Brand>
                    <Nav variant="pills" className="mr-auto"
                         onSelect={eventKey => this.selectUser(eventKey || null)}>
                        <Nav.Item>
                            <Nav.Link eventKey="" variant="secondary">
                                All Users
                            </Nav.Link>
                        </Nav.Item>
                        <NavDropdown title="Users" id="user_dropdown">
                            {users.map((user) =>
                                <NavDropdown.Item eventKey={user.user_id} key={user.user_id}>
                                    {user.username}
                                </NavDropdown.Item>
                            )}
                        </NavDropdown>
                    </Nav>
                    <Navbar.Collapse className="justify-content-end">
                        <Navbar.Text>
                            {this.state.user == null ? "" : `Viewing user #${this.state.user}`}
                        </Navbar.Text>
                    </Navbar.Collapse>
                </Navbar>
                {data}
            </div>
        );
    }
}

export default App;
