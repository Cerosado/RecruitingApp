import React from "react";
import {withRouter} from "react-router";
import {authFetch} from "../auth";
import ApplicationsList from "../ApplicationsList"

class Applications extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            postings: null,
            applicants: []
        }
    }

    componentDidMount() {
        let url_applicants = `http://localhost:5000/JobPosting`;
        authFetch(url_applicants)
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        postings: data
                    })
                },
                (error) => {
                    this.setState({
                        isLoaded: true,
                        error
                    });
                }
            );
    }

    render() {
        const { error, isLoaded, posting, applicants } = this.state;
        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>;
        } else {
            return (
                <ApplicationsList
                posting = {this.state.postings}
                />
            );
        }
    }
}

export default withRouter(Applications);
