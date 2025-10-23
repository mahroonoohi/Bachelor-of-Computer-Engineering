import React from "react";
import classes from "./UserAccount.module.scss";
import Profile from "../../images/user (2).png";
import Followers from "../../images/Multiple users silhouette.png";
import Followings from "../../images/Subscriber.png";
import Ideas from "../../images/IdeaIcon.png";

const UserAccount = ({
  profileImage,
  name,
  followers = 0,
  followings = 0,
  ideas = 0,
}) => {
  const changeUser = () => {
    window.location = `/showProfile/${name}`;
  };

  return (
    <div className={classes.container} onClick={changeUser}>
      <div className={classes.userInfo}>
        <img
          src={
            profileImage === null
              ? Profile
              : `http://api.iwantnet.space:8001${profileImage}`
          }
          alt="profile"
        />
        <p>{name}</p>
      </div>
      <div className={classes.userFeedback}>
        <div>
          <img className={classes.icon} src={Followers} alt="Followers" />
          {followers}
        </div>
        <div>
          <img className={classes.icon} src={Followings} alt="Followings" />
          {followings}
        </div>
        <div>
          <img className={classes.icon} src={Ideas} alt="Ideas" />
          {ideas}
        </div>
      </div>
    </div>
  );
};

export default UserAccount;
