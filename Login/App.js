import logo from './logo.svg';
import './App.css';
import LoginButton from './components/loginButton';
import LogoutButton from './components/logoutButton';
import UserProfile from './components/userProfile';

function App() {
  return (
    <div className="App">
      <div className="container">
      <br></br>
        <LoginButton/>
        <br></br>
        <LogoutButton/>
        <br></br>
        <UserProfile/>
      </div>
    </div>
  );
}

export default App;
