import React from "react";
import classes from "./Footer.module.scss";

const Footer = () => {
  return (
    <div className={classes.container}>
      <div className={classes.content}>
        <h3 className={classes.title}>Company</h3>
        <ul className={classes.options}>
          <li>
            <button>About Us</button>
          </li>
          <li>
            <button>Privacy Policy</button>
          </li>
          <li>
            <button>User Guid</button>
          </li>
        </ul>
      </div>
      <div className={classes.content}>
        <h3 className={classes.title}>Socials</h3>
        <ul className={classes.options}>
          <li>
            <button>Instagram</button>
          </li>
          <li>
            <button>Telegram</button>
          </li>
          <li>
            <button>Instagram</button>
          </li>
        </ul>
      </div>
      <div className={classes.content}>
        <h3 className={classes.title}>Contact Us</h3>
        <ul className={classes.options}>
          <li>031-37934528</li>
          <li>Privacy Policy</li>
          <li>Isfahan, University Of Isfahan</li>
        </ul>
      </div>
      <div className={classes.content}>
        <h3 className={`${classes.title} ${classes.smallTitle}`}>Ideagram</h3>
        <ul className={classes.options}>
          <li>All Rights Reserved.</li>
          <li>2023</li>
        </ul>
      </div>
    </div>
  );
};

export default Footer;
