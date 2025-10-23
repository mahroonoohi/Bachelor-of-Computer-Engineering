import React from "react";
import classes from "./Link.module.scss";
import Edit from "../../images/editBlack.png";
import Delete from "../../images/deleteBlack.png";

const Link = ({ linkNum, title }) => {
  return (
    <div className={classes.container}>
      <p className={classes.linkNum}>{linkNum}</p>
      <h4 className={classes.linkTitle}>{title}</h4>
      <button className={classes.editLink}>
        <img src={Edit} alt="Edit_Link" />
      </button>
      <button className={classes.deleteLink}>
        <img src={Delete} alt="Delete_Link" />
      </button>
    </div>
  );
};

export default Link;
