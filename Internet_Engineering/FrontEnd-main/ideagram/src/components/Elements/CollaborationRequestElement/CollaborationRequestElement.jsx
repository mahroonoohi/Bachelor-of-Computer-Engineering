import React from "react";
import classes from "./CollaborationRequestElement.module.scss";
import Delete from "../../../images/delete2.png";
import Edit from "../../../images/edit.png";
import { useDispatch } from "react-redux";
import { collaborationRequestsActions } from "../../../store/collaborationRequest";
import axios from "axios";

const CollaborationRequestElement = ({
  uuid,
  token,
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
  const dispatch = useDispatch();

  const deleteRequestHandler = async () => {
    await axios.delete(
      `${process.env.REACT_APP_API_ADDRESS}idea/collaboration/detail/${uuid}`,
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    dispatch(
      collaborationRequestsActions.deleteCollaborationRequest({
        uuid: uuid,
      })
    );
  };

  const manageEdit = async () => {
    await deleteRequestHandler();
    setJobTitle(jobTitle);
    setSkills(skills);
    setEducation(education);
    setAge(age);
    setSalary(salary);
    setStatus(status);
    setDescription(description);
  };

  return (
    <div className={classes.container}>
      <p>{amount}</p>
      <h4>{jobTitle}</h4>
      <button onClick={manageEdit}>
        <img src={Edit} alt="Edit" />
      </button>
      <button onClick={deleteRequestHandler}>
        <img src={Delete} alt="Delete" />
      </button>
    </div>
  );
};

export default CollaborationRequestElement;
