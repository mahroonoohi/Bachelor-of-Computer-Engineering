import React from "react";
import classes from "./LargeStepInfo.module.scss";

const LargeStepInfo = ({
  jobTitle,
  skills,
  education,
  age,
  salary,
  status,
  description,
}) => {
  return (
    <div className={classes.container}>
      <div>
        <label>Job Title</label>
        <p className={classes.text}>{jobTitle}</p>
      </div>
      <div>
        <label>Skills</label>
        <p className={classes.text}>{skills}</p>
      </div>
      <div>
        <label>Education</label>
        <p className={classes.text}>{education}</p>
      </div>
      <div>
        <label>Age</label>
        <p className={classes.shortText}>{age}</p>
      </div>
      <div>
        <label>Salary</label>
        <p className={classes.shortText}>{salary}</p>
      </div>
      <div>
        <label>Status</label>
        <p className={classes.shortText}>{status}</p>
      </div>
      <div>
        <label>Description</label>
        <p className={classes.longText}>{description}</p>
      </div>
    </div>
  );
};

export default LargeStepInfo;
