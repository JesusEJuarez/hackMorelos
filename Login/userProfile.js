import { useAuth0 } from "@auth0/auth0-react";
const redirectToForm = () => {
    console.log("Redirigiendo a Formulario.html");  // Mensaje para depuración
    window.location.href = "http://127.0.0.1:5000";
  };

function UserProfile() {
    const { user, isAuthenticated, isLoading } = useAuth0();
    

    if (isLoading) {
        return <div>Loading...</div>;
    }

    return (
        isAuthenticated && (
            <div>
                <br></br>
                <img src={user.picture} alt="User profile" />
                <h2>{user.name}</h2>
                Correo registrado:
                <div align="center">
                {user.email}</div>
                <br></br>
                <button onClick={redirectToForm}style={{ 
            backgroundColor: 'blue', 
            color: 'white', 
            padding: '20px 40px',
            marginRight: '10px', 
            border: 'none', 
            borderRadius: '5px',
            cursor: 'pointer'
        }}>
            
                    Registrar paciente.
                </button>
            </div>
        )
    );
}

export default UserProfile;
