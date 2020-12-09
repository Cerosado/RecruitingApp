import React from "react";
import './EventForm.css';
import DateTimePicker from "./DateTimeField";
import TextField from "@material-ui/core/TextField";
import Grid from '@material-ui/core/Grid';
import Dropdown from "./Dropdown";
import Button from "@material-ui/core/Button";
import jwtDecode from "jwt-decode";
import {authFetch} from "./auth";
import withRouter, {Link as RouterLink} from "react-router-dom";
import {withFormik} from "formik";


function EventForm ({
                        errors,
                        handleBlur,
                        handleChange,
                        handleSubmit,
                        touched,
                        values,
                        setFieldValue,
                        status
                    }) {

        return (
            <div>
                <h1>Create interview</h1>
                <form onSubmit={handleSubmit}>
                    <Grid   container
                            direction="row"
                            spacing={3}>
                        <Grid item xs={6}>
                            <TextField id="Location" label="Location" variant="outlined" required
                                       name="location"
                                       onChange={handleChange}
                                       onBlur={handleBlur}
                                       value={values.location}
                                       error={touched.location && Boolean(errors.location)}
                                       helperText={touched.location && errors.location}/>
                        </Grid>
                        <Grid item xs={6}>
                            <TextField
                                id="datetime-local"
                                label="Date"
                                type="datetime-local"
                                InputLabelProps={{
                                    shrink: true,
                                }}
                                name="date"
                                onChange={handleChange}
                                onBlur={handleBlur}
                                value={values.date}
                                error={touched.date && Boolean(errors.date)}
                                helperText={touched.date && errors.date}
                            />
                        </Grid>
                        <Grid item xs={12}>
                            <TextField id="AdditionalDetails" label="Additional details" variant="outlined"
                                       multiline
                                       rowsMax={4}
                                       required
                                       name="additionalDetails"
                                       onChange={handleChange}
                                       onBlur={handleBlur}
                                       value={values.additionalDetails}
                                       error={touched.additionalDetails && Boolean(errors.additionalDetails)}
                                       helperText={touched.additionalDetails && errors.additionalDetails}
                            />
                        </Grid>
                    </Grid>
                <br/>
                <br/>
                <br/>
                <div id="SubmitDiv">
                    <Button id="Submit" type="submit">Create interview</Button>
                </div>
                </form>
            </div>
        );
    }


const CreateEvent = withFormik({
    mapPropsToValues: () => ({
        location: '',
        date: '',
        additionalDetails: '',
    }),

    validate: values => {
        let errors = {};

        // if (!values.firstName) {
        //     errors.positionName = "Position name is required";
        // }
        // if (!values.location) {
        //     errors.location = "Location is required";
        // }
        // if (!values.description) {
        //     errors.description = "Description is required";
        // }
        // if (!values.keyDetails) {
        //     errors.keyDetails = "Key Details is required";
        // }
        return errors;
    },

    handleSubmit: (values, { props, setStatus} ) => {
        let opts = {
            location: values.location,
            date: values.date,
            additionalDetails: values.additionalDetails,
        }
        let user_id = jwtDecode(localStorage.getItem('jwt_token'))['id'];
        let url = `http://localhost:5000/EventForm`;

        authFetch(url, {
            method: 'post',
            body: JSON.stringify(opts)
        })
            .then(response => {
                if (!response.ok) {
                    throw response
                }
                return response.json()
            })
            .then(
                json_response => {
                    props.history.push({
                        pathname: `/JobPosting/${user_id}`,
                        state: {message: json_response.message, from: {pathname: "/"}},
                        from: '/'
                    });
                    console.log(json_response.message)
                }
            )
            .catch(error => {
                error.json().then(err => {
                    setStatus({
                        error: true,
                        msg: err.Error
                    })
                })
            })
    },
})(EventForm);

export default CreateEvent;


