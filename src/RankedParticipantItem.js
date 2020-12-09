import './RankedParticipantItem.css';
import React from "react";
import { Link as RouterLink } from 'react-router-dom';
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import * as PropTypes from "prop-types";
import icon from "./Resources/resume.jpg";
import Button from "@material-ui/core/Button";


function RankedParticipantItem(props) {
    const {name, university, to, gpa, resume, rank} = props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );

    return (
        <li>
            <ListItem button component={renderLink}>
                <ListItemText primary={name} style={{width: "70px"}}/>
                <ListItemText primary={university} style={{width: "185px"}}/>
                <ListItemText id='gpa' primary={gpa} style={{width: "70px"}}/>
                <Button
                    href={resume}
                    target="_blank"
                >
                    <img className='' src={icon} style={{width: "50px"}}/>
                </Button>
                <ListItemText primary={rank} style={{textAlign: "center", fontSize: "5 rem !important"}}/>
            </ListItem>
        </li>
    );
}

RankedParticipantItem.propTypes = {
    name: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    university: PropTypes.string.isRequired,
    gpa: PropTypes.string.isRequired,
    resume: PropTypes.string.isRequired,
    rank: PropTypes.number.isRequired,
};

export default RankedParticipantItem;