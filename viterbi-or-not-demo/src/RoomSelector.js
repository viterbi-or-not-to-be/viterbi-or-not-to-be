import React, {Component} from 'react';

export default class RoomSelector extends Component {
    constructor(props) {
        super(props);

        this.state = {
            username: '',
            room: ''
        }

        this.handleUsername = this.handleUsername.bind(this);
        this.handleRoom = this.handleRoom.bind(this);
        this.handleSubmit = this.handleSubmit.bind(this);
        this.handleCreateRoom = this.handleCreateRoom.bind(this);
        this.handleCopyRoom = this.handleCopyRoom.bind(this);
    }

    handleUsername(event) {
        this.setState({username: event.target.value});
    }

    handleRoom(event) {
        this.setState({room: event.target.value});
    }

    handleSubmit(event) {
        event.preventDefault();
        this.props.selectRoom(this.state.username, this.state.room);
    }

    handleCreateRoom(event) {
        this.props.createRoom(this.state.username);
    }

    handleCopyRoom(event) {
        this.props.copyRoom(this.state.username, event.target.value);
    }

    render() {
        return (
            <div id="room-selector-container">
                <div id="room-selector">
                    <form onSubmit={this.handleSubmit}>
                        <div id="room-selector-username">
                            <label>
                                <h2 className="form-label">Username</h2>
                                <div className="form-line">
                                    <input className="form-input" type="text" value={this.state.username} onChange={this.handleUsername} required />
                                </div>
                            </label>
                        </div>
                        <div id="room-selector-room">
                            <label>
                                <h2 className="form-label">Enter a Chatroom Code</h2>
                                <div className="form-line">
                                    <input className="form-input" type="number" value={this.state.room} onChange={this.handleRoom} min="1000" max="9999" required />
                                    <button className="submit-button" type="submit"><i className="material-icons">arrow_forward</i></button>
                                </div>
                            </label>
                            <div className="room-selector-section">
                                <h2 className="form-label">Create a new Room</h2>
                                <div className="room-selector-options">
                                    <button id="room-create" className="room-selector-button active-button" onClick={this.handleCreateRoom}><i className="material-icons">add</i>Create New</button>
                                </div>
                            </div>
                            <div className="room-selector-section">
                                <h2 className="form-label">Or Start From an Example</h2>
                                <div className="room-selector-options">
                                    <input className="room-selector-button" type="button" value="Dog Walking" onClick={this.handleCopyRoom} />
                                    <input className="room-selector-button" type="button" value="Throwing People Into Buckets" onClick={this.handleCopyRoom} />
                                    <input className="room-selector-button" type="button" value="We Broke the Fridge!" onClick={this.handleCopyRoom} />
                                    <input className="room-selector-button" type="button" value="Look at that Inequality" onClick={this.handleCopyRoom} />
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
            </div>
        )
    }
}