import { React, useState, useContext, useEffect } from "react";
import classes from "./Header.module.scss";
import Login from "../../images/login.png";
import Home from "../../images/home.png";
import User from "../../images/user.png";
import OptionsMenu from "../../images/userIcon.png";
import Menu from "../../images/burger-menu.png";
import { useLocation, Link } from "react-router-dom";
import AuthContext from "../../api/AuthContext";
import axios from "axios";
import { Skeleton } from "..";
import {
  SmallOptionsMenu,
  ProfileStructureSmallMenu,
  IdeaStructureSmallMenu,
  StepsStructureSmallMenu,
} from "../SmallMenus";

const Header = () => {
  const token = useContext(AuthContext).getAccessToken();
  console.log(token);

  const [isLoading, setIsLoading] = useState(true);
  const [isShowMenu, setIsShowMenu] = useState(false);
  const [isShowOptionsMenu, setIsShowOptionsMenu] = useState(false);

  const location = useLocation();
  const url = location.pathname.split("/")[1];

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
        setIsLoading(false);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const showMenuHandler = () => {
    setIsShowOptionsMenu(false);
    setIsShowMenu(!isShowMenu);
  };

  const showOptionsMenuHandler = () => {
    setIsShowMenu(false);
    setIsShowOptionsMenu(!isShowOptionsMenu);
  };

  return (
    <div className={classes.container}>
      <div className={classes.options}>
        <div className={classes.smallOptionsMenu}>
          <button
            className={classes.showOptionsMenuBTN}
            onClick={showOptionsMenuHandler}
          >
            <img src={OptionsMenu} alt="options_menu" />
          </button>
          <SmallOptionsMenu
            showOptionsMenuHandler={showOptionsMenuHandler}
            isShowOptionsMenu={isShowOptionsMenu}
          />
        </div>
        <div>
          <Link className={classes.btn} to="/login">
            <img src={Login} alt="login" />
          </Link>
        </div>
        <div>
          <Link className={classes.btn} to="/mainPage">
            <img src={Home} alt="home" />
          </Link>
        </div>
      </div>

      <div className={classes.title}>
        <h1>Ideagram</h1>
      </div>

      {isLoading ? (
        <Skeleton type="Toolbar" />
      ) : (
        <div className={classes.userInfo}>
          <Link to="/profileStructure/profile" className={classes.account}>
            <h4>{userName}</h4>
          </Link>
          <Link to="/profileStructure/profile" className={classes.profile}>
            <img
              src={
                userProfile === null
                  ? User
                  : `http://api.iwantnet.space:8001${userProfile}`
              }
              alt="user"
            />
          </Link>

          {(url === "profileStructure" ||
            url === "ideaStructure" ||
            url === "stepsStructure") && (
            <div className={classes.smallMenu}>
              <button className={classes.showMenuBTN} onClick={showMenuHandler}>
                <img src={Menu} alt="menu" />
              </button>

              {url === "profileStructure" && (
                <ProfileStructureSmallMenu
                  showMenuHandler={showMenuHandler}
                  isShowMenu={isShowMenu}
                />
              )}

              {url === "ideaStructure" && (
                <IdeaStructureSmallMenu
                  showMenuHandler={showMenuHandler}
                  isShowMenu={isShowMenu}
                />
              )}

              {url === "stepsStructure" && (
                <StepsStructureSmallMenu
                  showMenuHandler={showMenuHandler}
                  isShowMenu={isShowMenu}
                />
              )}
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Header;
