import React from "react";
import classes from "./StepInfo.module.scss";

const StepInfo = ({
  firstTitle,
  secTitle,
  thirdTitle,
  stepName,
  finishDate,
  description,
}) => {
  return (
    <div className={classes.container}>
      <div>
        <label>{firstTitle}</label>
        <p className={classes.shortText}>{stepName}</p>
      </div>
      <div>
        <label>{secTitle}</label>
        <p className={classes.shortText}>{finishDate}</p>
      </div>
      <div>
        <label>{thirdTitle}</label>
        <p className={classes.longText}>{description}</p>
      </div>
    </div>
  );
};

export default StepInfo;
