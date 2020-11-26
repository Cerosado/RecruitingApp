import React from "react";
import { Redirect, Route} from "react-router-dom";

export default function PrivateRoute({ children, ...rest}) {
    const [logged] = useAuth();
    console.log(logged);

    return (
        <Route {...rest} render={({location}) => {
            return logged
                ? children
                : <Redirect to={{pathname:'/login', state={from: location}}}/>
            }} />
    );
}
