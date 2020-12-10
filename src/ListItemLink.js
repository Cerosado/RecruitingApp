import React from "react";
import { Link as RouterLink } from 'react-router-dom';
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import * as PropTypes from "prop-types";

function ListItemLink(props) {
    const { icon, companyName, primary, to, location, deadline, isApplicant} = props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );

    return (
        <li>
            <ListItem button component={renderLink}>
                {icon ? <ListItemIcon>{icon}</ListItemIcon> : null}
                {isApplicant ? <ListItemText primary={companyName} /> : null}
                <ListItemText primary={primary}  style={{width: "100%"}}/>
                <ListItemText id='location' primary={location} />
                <ListItemText primary={deadline} />
            </ListItem>
        </li>
    );
}

ListItemLink.propTypes = {
    icon: PropTypes.element,
    primary: PropTypes.string.isRequired,
    to: PropTypes.string.isRequired,
    location: PropTypes.string.isRequired,
    deadline: PropTypes.string.isRequired,
};

export default ListItemLink;