import React, {useState, useEffect} from "react";
import ListItemLink from "./ListItemLink";
import List from "@material-ui/core/List";
import {Paper} from "@material-ui/core";
import './CompanyPostings.css';

// function JobPostingList() {
//     const [postingList, setPostingList] = useState([])
//
//
//     useEffect(() => {
//         fetch(url).then(response => response.json()).then(data => {
//            setPostingList(data.results);
//         });
//     })
//
//     return (
//         <div>
//             <ul>
//                 {postingList.map(posting => (
//                     <li key={posting.id}>{posting.position_name}</li>
//                 ))}
//             </ul>
//         </div>
//     );
// }

class JobPostingsList extends React.Component{
    constructor(props) {
        super(props);
        this.state = {
            error: null,
            isLoaded: false,
            postings: []
        };
    }

    componentDidMount() {
        let url = 'http://localhost:5000/JobPosting?user_id=2';
        fetch(url)
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        postings: data
                    });
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
        const { error, isLoaded, postings } = this.state;

        if (error) {
            return <div>Error: {error.message}</div>;
        } else if (!isLoaded) {
            return <div>Loading...</div>
        } else {
            return (
                <Paper className='jobPostingsList' elevation={0}>
                    <h1>My Job Postings</h1>
                    {/*<div><p>Select job posting to see ranked applicants</p></div>*/}
                    <List>
                        {postings.map(posting => (
                            <ListItemLink
                                key={posting.posting_id}
                                primary={posting.position_name}
                                to={'/jobPostings/' + posting.id}
                            >
                            </ListItemLink>
                        ))}
                    </List>
                </Paper>
            );
        }
    }
}

export default JobPostingsList;
