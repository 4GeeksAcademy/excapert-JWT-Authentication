import React, { useContext, useState } from "react";
import rigoImageUrl from "../../img/rigo-baby.jpg";
import "../../styles/home.css";
import { useNavigate } from 'react-router-dom';

export const Signup = () => {
	// const [username, setUsername] = useState("");
	const [email, setEmail] = useState("");
	const [password, setPassword] = useState("");
	const navigate = useNavigate();
  
	const handleClick = () => {
	  const opts = {
		method: "POST",
		headers: {
		  "Content-Type": "application/json",
		},
		body: JSON.stringify({
		  email: email,
		  password: password,
		}),
	  };
  
	  fetch(process.env.BACKEND_URL+"/api/signup", opts)
		.then((resp) => {
		  if (resp.status === 200) return resp.json();
		  else alert("Error.");
		})
		.then((data) => {
		  console.log(data);
		 
		  navigate("/login"); 
		})
	  };

	return (
<div className="text-center">
      <h1>Sign Up</h1>
      <div>
        <input
          type="text"
          placeholder="email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
        />
        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
        />
        <button onClick={handleClick}>Sign Up</button>
        <button onClick={() => navigate('/')}>Home page</button>
        <button onClick={() => navigate('/login')}>Login</button>
      </div>
    </div>
  );
};