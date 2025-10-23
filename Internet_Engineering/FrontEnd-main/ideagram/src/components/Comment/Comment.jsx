import React from "react";
import classes from "./Comment.module.scss";
import UserProfile from "../../images/user (2).png";

const Comment = ({ profile, text }) => {
  return (
    <div className={classes.body}>
      <img
        src={
          profile === null
            ? UserProfile
            : `http://api.iwantnet.space:8001${profile}`
        }
        alt="profile"
      />
      <p>{text}</p>
    </div>
  );
};

export default Comment;
