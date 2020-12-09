import Container from "@material-ui/core/Container";
import CssBaseline from "@material-ui/core/CssBaseline";
import Grid from "@material-ui/core/Grid";
import jwtDecode from "jwt-decode";
import Button from "@material-ui/core/Button";
import {withFormik} from "formik";
import {authFetch} from "./auth";
import React, {useEffect} from "react";
import {useParams} from "react-router-dom";

function JobPostingForm({
                            errors,
                            handleBlur,
                            handleChange,
                            handleSubmit,
                            touched,
                            values,
                            setFieldValue,
                            status
                        }) {
    const [posting, setPosting] = React.useState('');
    const { id } = useParams();
    useEffect(() => {

        let url = `http://localhost:5000/JobPostingForm/${id}`;
        authFetch(url, {
            method: 'get'
        })
            .then(response => response.json())
            .then(
                (data) => {
                    // this.setState({
                        setPosting(data);
                        // companyName: data.companyName,
                        // positionName: data.positionName,
                        // location: data.location,
                        // description: data.description,
                        // keyDetails: data.keyDetails,
                        // payType: data.payType,
                        // payAmount: data.payAmount,
                        // deadline: data.deadline,
                    // })
                },
                // (error) => {
                //     this.setState({
                //         isLoaded: true,
                //         error
                //     });
                // }
    )}, [id]);
        // const { companyName,
        //     positionName,
        //     location,
        //     description,
        //     keyDetails,
        //     payType,
        //     payAmount,
        //     deadline,} = this.state;
    return (
        <Container component="main" >
            <CssBaseline />
            <h1>Create Job Posting</h1>
            <form onSubmit={handleSubmit}>
                <Grid   container
                        direction="row"
                        justify="center"
                        alignItems="center"
                        spacing={2}>
                    <Grid item xs={4}>
                        <h2 id="CompanyName">
                            Company name:
                        </h2>
                        <h3>{posting.first_name}</h3>
                    </Grid>
                    <Grid item xs={4}>
                        <h2 id="PositionName">
                            Position name:
                        </h2>
                        <h3>{posting.position_name}</h3>
                    </Grid>
                    <Grid item xs={4}>
                        <h2 id="Location">
                            Location:
                        </h2>
                        <h3>{posting.location}</h3>
                    </Grid>
                    <Grid item xs>
                        <h2 id="Description">
                            Description:
                        </h2>
                        <h3>{posting.description}</h3>
                    </Grid>
                    <Grid item xs>
                        <h2 id="KeyDetails">
                            Key details:
                        </h2>
                        <h3>{posting.key_details}</h3>
                    </Grid>
                    <Grid item xs={4}>
                        <h2 id="PayType">
                            Pay type:
                        </h2>
                        <h3>{posting.pay_type}</h3>
                    </Grid>
                    <Grid item xs={4}>
                        <h2 id="PayAmount">
                            Pay amount:
                        </h2>
                        <h3>{posting.pay_amount}</h3>
                    </Grid>

                    <Grid id='DatetimeGrid' item xs={4}>
                        <h2 id="Deadline">
                            Deadline:
                        </h2>
                        <h3>{posting.deadline}</h3>
                    </Grid>
                </Grid>
                <br/>
                <br/>
                <br/>
                <div id="SubmitDiv">
                    <Grid item xs={12} sm={12}>
                            <Button id='submit_button' type="submit" variant="contained" color="primary"
                                    disabled={jwtDecode(localStorage.getItem('jwt_token'))['rls'] === 'recruiter'}>
                                Apply
                            </Button>
                    </Grid>
                </div>
            </form>
        </Container>
    );
}

const CreateJobPosting = withFormik({
    // mapPropsToValues: () => ({
    //     posting_id: '',
    //     location: '',
    //     description: '',
    //     keyDetails: '',
    //     payType: '',
    //     payAmount: '',
    //     deadline: '',
    // }),

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
            let url = `http://localhost:5000/Applications/${props.match.params.id}`;
            authFetch(url, {
                method: 'post',
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
                            pathname: '/JobPostings',
                            state: {message: json_response.message, from: {pathname: "/"}},
                            from: '/'
                        });
                        console.log(json_response.message)
                    }
                )
    },
})(JobPostingForm);

export default CreateJobPosting;
