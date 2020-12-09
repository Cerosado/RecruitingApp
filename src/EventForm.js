import React from "react";
import './EventForm.css';
import DateTimePicker from "./DateTimeField";
import TextField from "@material-ui/core/TextField";
import Grid from '@material-ui/core/Grid';
import Dropdown from "./Dropdown";
import Button from "@material-ui/core/Button";
import jwtDecode from "jwt-decode";

export default class EventForm extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            PositionName: null,
            Location: null,
            Description: null,
            KeyDetails: null,
            PayType: null,
            PayAmount: null,
            Deadline: null,
        };
    }

    render() {
            return (
                <div>
                    <h1>Create interview</h1>
                    <form>
                        <Grid   container
                                direction="row"
                                spacing={3}>
                            <Grid item xs={6}>
                                <TextField id="Location" label="Location" variant="outlined" required/>
                            </Grid>
                            <Grid item xs={6}>
                                <DateTimePicker
                                    label='Date'>
                                </DateTimePicker>
                            </Grid>
                            <Grid item xs={12}>
                                <TextField id="AdditionalDetails" label="Additional details" variant="outlined"
                                           multiline
                                           rowsMax={4}
                                           required/>
                            </Grid>
                        </Grid>
                    </form>
                    <br/>
                    <br/>
                    <br/>
                    <div id="SubmitDiv">
                        <Button id="Submit" type="submit">Create job posting</Button>
                    </div>
                </div>
            );
    }
}

