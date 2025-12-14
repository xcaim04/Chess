import { useState } from "react";
import Login from "./components/Login";
import ChessApp from "./components/ChessApp";

function isTokenValid(token) {
  try {
    const payload = JSON.parse(atob(token.split(".")[1]));
    return payload.exp * 1000 > Date.now();
  } catch {
    return false;
  }
}

export default function App() {
  const saved = localStorage.getItem("jwt");
  const [token, setToken] = useState(
    saved && isTokenValid(saved) ? saved : null
  );

  console.log(token);

  if (!token) {
    return (
      <Login
        onLogin={(newToken) => {
          localStorage.setItem("jwt", newToken);
          setToken(newToken);
        }}
      />
    );
  }

  return <ChessApp token={token} />;
}
