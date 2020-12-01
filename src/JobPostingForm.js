import React from "react";
import './JobPostingForm.css';
import DateTimePicker from "./DateTimeField";
import TextField from "@material-ui/core/TextField";
import Grid from '@material-ui/core/Grid';
import Dropdown from "./Dropdown";
import Button from "@material-ui/core/Button";

export default class JobPostingForm extends React.Component {
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
                <h1>Create Job Posting</h1>
                <form>
                    <Grid   container
                            direction="row"
                            justify="center"
                            alignItems="center">
                        <Grid item xs>
                            <TextField id="PositionName" label="Position name" variant="outlined" required/>
                        </Grid>

                        <Grid item xs>
                            <TextField id="Location" label="Location" variant="outlined" required/>
                        </Grid>

                        <TextField id="Description" label="Description" variant="outlined" required/>
                        <TextField id="KeyDetails" label="Key Details" variant="outlined" required/>
                        <Grid item xs>
                            <TextField id="PayType" label="Pay Type" variant="outlined"/>
                        </Grid>
                        <Grid item xs>
                            <TextField id="PayAmount" label="Pay Amount" variant="outlined"/>
                        </Grid>
                        <Grid id='DatetimeGrid' item xs>
                            <DateTimePicker></DateTimePicker>
                        </Grid>
                    </Grid>
                    <h1>Resume ranking settings:</h1>
                    <Grid   container
                            direction="row"
                            justify="center"
                            alignItems="center">
                        <Grid item xs>
                            <Dropdown label={"Education"}
                                      menuItems={[{weight: 30, label: "Very important"},
                                                  {weight: 20, label: "Important"},
                                                  {weight: 10, label: "Not important"},]}>
                            </Dropdown>
                        </Grid>
                        <Grid item xs>
                            <Dropdown label={"Experience"}
                                      menuItems={[{weight: 30, label: "Very important"},
                                          {weight: 20, label: "Important"},
                                          {weight: 10, label: "Not important"},]}>
                            </Dropdown>
                        </Grid>
                        <Grid item xs>
                            <Dropdown label={"Skills"}
                                      menuItems={[{weight: 1, label: "Software development"},
                                          {weight: 2, label: "Finance"},
                                          {weight: 3, label: "Human resources"},]}>
                            </Dropdown>
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

