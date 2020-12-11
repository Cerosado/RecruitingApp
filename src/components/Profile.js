import React from "react";
import TextField from '@material-ui/core/TextField';
import Button from '@material-ui/core/Button';
import Card from "@material-ui/core/Card";
import Divider from "@material-ui/core/Divider";
import CardContent from "@material-ui/core/CardContent";
import Typography from "@material-ui/core/Typography";
import {withRouter} from "react-router";
import {authFetch} from "../auth";
import FileUpload from "../fileUpload"

class Profile extends React.Component {
    constructor(props) {
        super(props);
        this.state = {
            isLoaded: false,
            error:null,
            profile: {},
            emailValue: '',
            isUpdating:true
        };
    }
    changeEmail = () => {
        this.setState({
            isLoaded: true,
            profile: this.state.profile,
            emailValue: this.state.emailValue,
            isUpdating:false
        })
    }
    saveTextField = (e) => {
        this.setState({
            isLoaded: true,
            profile:this.state.profile,
            emailValue: e.target.value,
            isUpdating:false
        })
    }
    submitEmail = ()=>{
        let url = `http://localhost:5000/update/email`;
        authFetch(url, {
            method: 'POST',
            body: JSON.stringify({'email':this.state.emailValue})
        }).then(r => r.json())
            this.setState({
                isLoaded: true,
                profile: this.state.profile,
                emailValue:this.state.emailValue,
                isUpdating:true
            });
    }

    componentDidMount() {
        let url = `http://localhost:5000/Profile`;
        authFetch(url)
            .then(response => response.json())
            .then(
                (data) => {
                    this.setState({
                        isLoaded: true,
                        profile: data,
                        emailValue: data['email'],
                        isUpdating:true
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
    if (this.state.error) {
        return <div>Error: {this.state.error.message}</div>;
    } else if (!this.state.isLoaded) {
        return <div>Loading...</div>;
    } else {
        return (
            <div style={{paddingTop:"10px", paddingBottom:"10px", marginTop:"30px"}}>
            <Card variant="outlined" >
                <CardContent>
                    <Typography fullWidth className='names' variant="h5" component="h3">
                            First & Last Names: <Divider/>{this.state.profile.first_name} {this.state.profile.last_name}
                    </Typography>
                </CardContent>
            </Card> <Card variant="outlined">
            <CardContent>
                    <Typography className='role' variant="h5" component="h2">
                        Username: <Divider/>{this.state.profile.username}
                    </Typography>
            </CardContent>
            </Card>
            <Card variant="outlined">
            <CardContent>
                    <Typography className='role' variant="h5" component="h2">
                        Role: <Divider/>{this.state.profile.roles}
                    </Typography>
            </CardContent>
            </Card>
            <Card variant="outlined">
            <CardContent>
                    <Typography className='role' variant="h5" component="h2">
                        Resume: <Divider/><FileUpload/>
                    </Typography>
            </CardContent>
            </Card>
            <Card variant="outlined">
            <CardContent>
                    <Typography className='email' variant="h5" component="h2">
                        Email: <Divider/>
                    </Typography>
                {this.state.isUpdating?
                <div>
                <Divider bottomMargin/>
                <div className='container' style={{display:"flex"}}><Typography variant="h5" component="h2">{this.state.emailValue}</Typography>
                <Button
                type="update"
                variant="contained"
                color="primary"
                style={{height: '30px', width : '150px', marginLeft:"auto"}}
                onClick={this.changeEmail}
                >
                Update Email
                </Button>
                </div>
                </div>
                :
                <div className='container' style={{display:"flex"}}>
                <TextField
                variant="outlined"
                margin="normal"
                required
                fullWidth
                name="newEmail"
                type="email"
                id="email"
                value={this.state.emailValue}
                onChange={this.saveTextField}
                />
                <Button
                type="update"
                variant="contained"
                color="primary"
                style={{height:40, left:"4px", top:"26px"}}
                onClick={this.submitEmail}
                >
                    Submit
                </Button>
                </div>}
                </CardContent>
            </Card>
            </div>
        );
    }
}
}


export default withRouter(Profile);
