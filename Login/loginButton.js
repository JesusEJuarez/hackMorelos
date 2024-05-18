import { useAuth0 } from "@auth0/auth0-react";


function LogginButton(){
    const{loginWithRedirect}=useAuth0();

    return(
        <button onClick={()=> loginWithRedirect()}style={{ 
            backgroundColor: 'green', 
            color: 'white', 
            padding: '20px 40px',
            marginRight: '10px', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
        }}>Log in</button>
    )

};
export default LogginButton;