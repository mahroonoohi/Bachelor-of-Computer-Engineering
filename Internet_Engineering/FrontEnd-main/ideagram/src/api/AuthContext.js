import { React, createContext, useState } from "react";
import axios from "axios";
import jwt_decode from "jwt-decode";
import { useNavigate } from "react-router-dom";

const AuthContext = createContext();

export const AuthContextProvider = ({ children }) => {
  const [user, setUser] = useState(() => {
    if (localStorage.getItem("tokens")) {
      let tokens = JSON.parse(localStorage.getItem("tokens"));
      return jwt_decode(tokens.access);
    }
    return null;
  });

  const getAccessToken = () => {
    if (localStorage.getItem("tokens")) {
      let tokens = JSON.parse(localStorage.getItem("tokens"));
      return tokens.access;
    }
    return null;
  };

  const navigate = useNavigate();

  const login = async (payload) => {
    console.log(payload);
    const apiResponse = await axios.post(
      `${process.env.REACT_APP_API_ADDRESS}auth/jwt/login/`,
      payload
    );
    console.log(apiResponse);
    localStorage.setItem("tokens", JSON.stringify(apiResponse.data));
    setUser(jwt_decode(apiResponse.data.access));
    navigate("/mainPage");
    return apiResponse.data.access;
  };

  const register = async (payload) => {
    console.log(payload);
    const apiResponse = await axios.post(
      `${process.env.REACT_APP_API_ADDRESS}user/register/`,
      payload
    );
    console.log(apiResponse.data.token);
    localStorage.setItem("tokens", JSON.stringify(apiResponse.data.token));
    setUser(jwt_decode(apiResponse.data.token.access));
    navigate("/mainPage");
  };

  return (
    <AuthContext.Provider value={{ user, getAccessToken, login, register }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
