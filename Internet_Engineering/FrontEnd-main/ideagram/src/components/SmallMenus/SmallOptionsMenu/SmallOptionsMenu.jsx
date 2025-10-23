import { React, useState, useContext, useEffect } from "react";
import classes from "./SmallOptionsMenu.module.scss";
import User from "../../../images/user.png";
import Login from "../../../images/login.png";
import Home from "../../../images/home.png";
import { useLocation, Link } from "react-router-dom";
import AuthContext from "../../../api/AuthContext";
import axios from "axios";

const SmallOptionsMenu = ({ showOptionsMenuHandler, isShowOptionsMenu }) => {
  const token = useContext(AuthContext).getAccessToken();
  console.log(token);

  const [userProfile, setUserProfile] = useState(null);
  const [userName, setUserName] = useState(null);

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        setUserProfile(res.data.profile_image);
        setUserName(res.data.username);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  return (
    <ul
      className={`${(showOptionsMenuHandler, classes.optionsMenu)} ${
        isShowOptionsMenu ? classes.visible : classes.invisible
      }`}
    >
      <li onClick={showOptionsMenuHandler} className={classes.userProfile}>
        <Link to="/profileStructure/profile" className={classes.profile}>
          <img
            src={
              userProfile === null
                ? User
                : `http://api.iwantnet.space:8001${userProfile}`
            }
            alt="user"
          />
          <h4>{userName}</h4>
        </Link>
      </li>
      <li onClick={showOptionsMenuHandler}>
        <Link className={classes.btn} to="/login">
          <img src={Login} alt="login" />
        </Link>
      </li>
      <li onClick={showOptionsMenuHandler}>
        <Link className={classes.btn} to="/mainPage">
          <img src={Home} alt="home" />
        </Link>
      </li>
    </ul>
  );
};

export default SmallOptionsMenu;
