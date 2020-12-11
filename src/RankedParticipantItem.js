import './RankedParticipantItem.css';
import React from "react";
import { Link as RouterLink } from 'react-router-dom';
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import * as PropTypes from "prop-types";
import icon from "./Resources/resume.png";
import Button from "@material-ui/core/Button";
import Grid from "@material-ui/core/Grid";
import Typography from "@material-ui/core/Typography";


function RankedParticipantItem(props) {
    const {name, to, resume, rank} = props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );

    return (
        <li>
                <Grid   container
                        direction="row"
                        alignItems="center"
                        spacing={1}>
                    <ListItem button component={renderLink} style={{width: "75%"}}>
                        <Grid item xs={10}>
                            <ListItemText primary={name} />
                        </Grid>
                        <Grid item xs={2} style={{textAlign: "center !important"}}>
                            <ListItemText primary={rank} style={{width: "100% !important"}}/>
                        </Grid>
                    </ListItem>
            <Grid item xs={3} style={{textAlign: "center"}}>
                <Button
                    href={resume}
                    target="_blank">
                    <img className='' src={icon} style={{width: "50px"}} />
                </Button>
            </Grid>
                </Grid>

        </li>
    );
}

RankedParticipantItem.propTypes = {
    name: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    resume: PropTypes.string.isRequired,
    rank: PropTypes.number.isRequired,
};

export default RankedParticipantItem;