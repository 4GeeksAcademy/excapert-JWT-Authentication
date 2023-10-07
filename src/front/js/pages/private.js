import React from "react";

function logout() {

	localStorage.removeItem("token");
	console.log("loging out");
	window.location.reload(false);

}


const Private = () => {
  return (
    <div>
      <h1>You're in!</h1>
	  <button className="btn btn-secondary" onClick={()=>logout()}>Log Out</button>
    </div>
  );
};

export default Private;
