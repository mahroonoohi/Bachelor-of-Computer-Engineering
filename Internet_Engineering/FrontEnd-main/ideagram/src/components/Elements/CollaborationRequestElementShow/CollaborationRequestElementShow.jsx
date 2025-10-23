import React from "react";
import classes from "./CollaborationRequestElementShow.module.scss";

const CollaborationRequestElementShow = ({
  amount,
  jobTitle,
  skills,
  education,
  age,
  salary,
  status,
  description,
  setJobTitle,
  setSkills,
  setEducation,
  setAge,
  setSalary,
  setStatus,
  setDescription,
}) => {
  const display = async () => {
    setJobTitle(jobTitle);
    setSkills(skills);
    setEducation(education);
    setAge(age);
    setSalary(salary);
    setStatus(status);
    setDescription(description);
  };

  return (
    <div className={classes.container} onClick={display}>
      <p>{amount}</p>
      <h4>{jobTitle}</h4>
    </div>
  );
};

export default CollaborationRequestElementShow;
