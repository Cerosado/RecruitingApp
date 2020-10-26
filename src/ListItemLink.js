import React from "react";
import { Link as RouterLink } from 'react-router-dom';
import ListItem from "@material-ui/core/ListItem";
import ListItemIcon from "@material-ui/core/ListItemIcon";
import ListItemText from "@material-ui/core/ListItemText";
import * as PropTypes from "prop-types";

function ListItemLink(props) {
    const { icon, primary, to, location, presentationDate, deadline} = props;

    const renderLink = React.useMemo(
        () => React.forwardRef((itemProps, ref) => <RouterLink to={to} ref={ref} {...itemProps} />),
        [to],
    );

    return (
        <li>
            <ListItem button component={renderLink}>
                {icon ? <ListItemIcon>{icon}</ListItemIcon> : null}
                <ListItemText primary={primary} />
                <ListItemText primary={location} />
                <ListItemText primary={presentationDate} />
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
    presentationDate: PropTypes.string.isRequired,
    deadline: PropTypes.string.isRequired,
};

export default ListItemLink;