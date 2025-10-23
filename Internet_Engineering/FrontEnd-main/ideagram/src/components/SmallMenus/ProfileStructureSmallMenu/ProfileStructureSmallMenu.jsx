import React from "react";
import classes from "./ProfileStructureSmallMenu.module.scss";
import MyProfile from "../../../images/MyProfile.png";
import My_Idea from "../../../images/MyIdea.png";
import Saved_Ideas from "../../../images/SavedIdeas.png";
import Follower from "../../../images/Follower.png";
import Following from "../../../images/Following.png";
import Edit_Profile from "../../../images/EditProfile.png";
import CreateIdeaIMG from "../../../images/CreateIdea.png";
import { Link } from "react-router-dom";

const ProfileStructureSmallMenu = ({ showMenuHandler, isShowMenu }) => {
  return (
    <ul
      className={`${classes.menu} ${
        isShowMenu ? classes.visible : classes.invisible
      }`}
    >
      <li onClick={showMenuHandler}>
        <Link className={classes.sidebarOptions} to="/profileStructure/profile">
          <img src={MyProfile} alt="Profile" /> Profile
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/editProfile"
        >
          <img src={Edit_Profile} alt="Edit_Profile" /> Edit Profile
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/createIdea"
        >
          <img src={CreateIdeaIMG} alt="Create_Idea" /> Create Idea
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link className={classes.sidebarOptions} to="/profileStructure/myIdeas">
          <img src={My_Idea} alt="My_Ideas" /> My Ideas
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/savedIdeas"
        >
          <img src={Saved_Ideas} alt="Saved_Ideas" /> Saved Ideas
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/followers"
        >
          <img src={Follower} alt="Follower" /> Followers
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/followings"
        >
          <img src={Following} alt="Following" /> Followings
        </Link>
      </li>
    </ul>
  );
};

export default ProfileStructureSmallMenu;
