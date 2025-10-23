import React from "react";
import classes from "./SelectableItemToShow.module.scss";

const SelectableItemToShow = ({ amount, title }) => {
  return (
    <div className={classes.container}>
      <p>{amount}</p>
      <h4>{title}</h4>
    </div>
  );
};

export default SelectableItemToShow;
