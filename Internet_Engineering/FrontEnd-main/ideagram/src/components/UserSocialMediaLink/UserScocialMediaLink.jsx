import React from "react";
import Telegram from "../../images/Telegram.png";
import Linkedin from "../../images/Linkedin.png";
import Facebook from "../../images/facebook.png";
import Github from "../../images/Github.png";
import Instagram from "../../images/Instagram.png";
import Gitlab from "../../images/gitlab.png";
import Twitter from "../../images/twitter.png";
import classes from "./UserSocialMediaLink.module.scss";

const UserSocialMediaLink = ({ type, link }) => {
  console.log(type, link);
  return (
    <a
      className={classes.container}
      href={link}
      target="_blank"
      rel="noopener noreferrer"
    >
      {
        {
          github: <img src={Github} alt="github" />,
          gitlab: <img src={Gitlab} alt="gitlab" />,
          telegram: <img src={Telegram} alt="telegram" />,
          linkedin: <img src={Linkedin} alt="linkedin" />,
          instagram: <img src={Instagram} alt="instagram" />,
          facebook: <img src={Facebook} alt="facebook" />,
          twitter: <img src={Twitter} alt="twitter" />,
        }[type]
      }
    </a>
  );
};

export default UserSocialMediaLink;
