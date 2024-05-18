import { useAuth0 } from "@auth0/auth0-react";

function LogoutButton(){
    const{logout}=useAuth0();

    return(
        <button onClick={()=> logout({ returnTo: window.location.origin })}style={{ 
            backgroundColor: 'red', 
            color: 'white', 
            padding: '20px 40px',
            marginRight: '10px', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
        }}>Log out</button>
    )

};
export default LogoutButton;