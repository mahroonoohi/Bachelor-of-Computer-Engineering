import React from "react";
import classes from "./UserFeedbackSmallMenu.module.scss";
import FollowersWhiteIcon from "../../../images/FollowersWhite.png";
import FollowingsWhiteIcon from "../../../images/FollowingsWhite.png";
import IdeaWhiteIcon from "../../../images/IdeaWhite.png";

const UserFeedbackSmallMenu = ({ showMenuHandler, isShowMenu }) => {
  return (
    <ul
      className={`${classes.menu} ${
        isShowMenu ? classes.visible : classes.invisible
      }`}
    >
      <li onClick={() => showMenuHandler("ideas")}>
        <button>
          <img src={IdeaWhiteIcon} alt="Ideas" />
          Ideas
        </button>
      </li>
      <li onClick={() => showMenuHandler("followers")}>
        <button>
          <img src={FollowersWhiteIcon} alt="Followers" />
          Followers
        </button>
      </li>
      <li onClick={() => showMenuHandler("followings")}>
        <button>
          <img src={FollowingsWhiteIcon} alt="Followings" />
          Followings
        </button>
      </li>
    </ul>
  );
};

export default UserFeedbackSmallMenu;
