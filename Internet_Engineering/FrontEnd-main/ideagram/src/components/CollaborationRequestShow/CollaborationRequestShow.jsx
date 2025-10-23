import { React, useEffect, useState } from "react";
import classes from "./CollaborationRequestShow.module.scss";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { collaborationRequestsActions } from "../../store/collaborationRequest";
import CollaborationRequestElementShow from "../Elements/CollaborationRequestElementShow/CollaborationRequestElementShow";
import LargeStepInfo from "../LargeStepInfo/LargeStepInfo";

const CollaborationRequestShow = ({ uuid, token }) => {
  const dispatch = useDispatch();
  const requests = useSelector(
    (state) => state.collaborationRequests.collaborationRequests
  );
  const requestsNum = useSelector(
    (state) => state.collaborationRequests.collaborationRequestsNum
  );

  const [jobTitle, setJobTitle] = useState("");
  const [skills, setSkills] = useState("");
  const [education, setEducation] = useState("");
  const [age, setAge] = useState("");
  const [salary, setSalary] = useState("");
  const [status, setStatus] = useState("");
  const [description, setDescription] = useState("");

  useEffect(() => {
    const getIdeaData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/collaboration/${uuid}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        dispatch(collaborationRequestsActions.deleteAll());
        for (const item of res.data) {
          dispatch(
            collaborationRequestsActions.addCollaborationRequest({
              uuid: item.uuid,
              jobTitle: item.title,
              skills: item.skills,
              education: item.education,
              age: item.age,
              salary: item.salary,
              status: item.status,
              description: item.description,
            })
          );
        }

        setJobTitle(res.data[0].title);
        setSkills(res.data[0].skills);
        setEducation(res.data[0].education);
        setAge(res.data[0].age);
        setSalary(res.data[0].salary);
        setStatus(res.data[0].status);
        setDescription(res.data[0].description);
      } catch (err) {
        console.log(err);
      }
    };
    getIdeaData();
  }, []);

  return (
    <div className={classes.body}>
      <h2>Collaboration Request</h2>
      <div className={classes.collaborationRequests}>
        <h4 className={classes.title}>
          Collaboration
          <br /> Table
        </h4>
        {requestsNum !== 0 && (
          <div className={classes.collaborationRequestsList}>
            {requests.map((item, index) => (
              <CollaborationRequestElementShow
                key={index}
                amount={index + 1}
                jobTitle={item.jobTitle}
                skills={item.skills}
                education={item.education}
                age={item.age}
                salary={item.salary}
                status={item.status}
                description={item.description}
                setJobTitle={setJobTitle}
                setSkills={setSkills}
                setEducation={setEducation}
                setAge={setAge}
                setSalary={setSalary}
                setStatus={setStatus}
                setDescription={setDescription}
              />
            ))}
          </div>
        )}
      </div>
      <div className={classes.collaborationsInfoContainer}>
        <h4 className={classes.title}>
          Collaboration
          <br />
          Information
        </h4>

        <div className={classes.collaborationsInfo}>
          <LargeStepInfo
            jobTitle={jobTitle}
            skills={skills}
            education={education}
            age={age}
            salary={salary}
            status={status}
            description={description}
          />
        </div>
      </div>
    </div>
  );
};

export default CollaborationRequestShow;
