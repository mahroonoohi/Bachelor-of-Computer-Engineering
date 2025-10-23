import { React, useState, useEffect } from "react";
import classes from "./CollaborationRequest.module.scss";
import Add from "../../images/add.png";
import CollaborationRequestElement from "../Elements/CollaborationRequestElement/CollaborationRequestElement";
import { useDispatch, useSelector } from "react-redux";
import { collaborationRequestsActions } from "../../store/collaborationRequest";
import axios from "axios";

const CollaborationRequest = ({ uuid, token }) => {
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
  const [status, setStatus] = useState("full_time");
  const [description, setDescription] = useState("");

  useEffect(() => {
    const getUserData = async () => {
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
        for (const req of res.data) {
          dispatch(
            collaborationRequestsActions.addCollaborationRequest({
              uuid: req.uuid,
              jobTitle: req.title,
              skills: req.skills,
              education: req.education,
              age: req.age,
              salary: req.salary,
              status: req.status,
              description: req.description,
            })
          );
        }
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const addRequest = async () => {
    if (
      jobTitle !== "" &&
      skills !== "" &&
      education !== "" &&
      age !== "" &&
      age !== "" &&
      salary !== "" &&
      status !== "" &&
      description !== ""
    ) {
      try {
        const res = await axios.post(
          `${process.env.REACT_APP_API_ADDRESS}idea/collaboration/${uuid}`,
          {
            title: jobTitle,
            status: status,
            skills: skills,
            age: age,
            education: education,
            description: description,
            salary: salary,
          },
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        dispatch(
          collaborationRequestsActions.addCollaborationRequest({
            uuid: res.data.uuid,
            jobTitle: res.data.title,
            skills: res.data.skills,
            education: res.data.education,
            age: res.data.age,
            salary: res.data.salary,
            status: res.data.status,
            description: res.data.description,
          })
        );
        console.log(requests);
        setJobTitle("");
        setSkills("");
        setEducation("");
        setAge("");
        setSalary("");
        setStatus("full_time");
        setDescription("");
      } catch (err) {
        console.log(err);
      }
    } else {
      alert("Please fill the fields properly");
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.body}>
        <h2>
          Collaboration <br /> Request
        </h2>
        <div className={classes.collaborationInfo}>
          <div className={classes.collaborationDetails}>
            <h3>Collaborator Information</h3>
            <div className={classes.details}>
              <div>
                <label>Job Title</label>
                <input
                  type="text"
                  value={jobTitle}
                  onChange={(e) => {
                    setJobTitle(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Skills</label>
                <input
                  type="text"
                  value={skills}
                  onChange={(e) => {
                    setSkills(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Education</label>
                <input
                  type="text"
                  value={education}
                  onChange={(e) => {
                    setEducation(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Age</label>
                <input
                  type="number"
                  min={0}
                  className={classes.short}
                  value={age}
                  onChange={(e) => {
                    setAge(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Salary</label>
                <input
                  type="number"
                  min={0}
                  className={classes.short}
                  value={salary}
                  onChange={(e) => {
                    setSalary(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Status</label>
                <select
                  name="status"
                  onChange={(e) => {
                    setStatus(e.target.value);
                  }}
                >
                  <option value="full_time" selected>
                    Full-Time
                  </option>
                  <option value="part_time">Part-Time</option>
                  <option value="other">Other</option>
                </select>
              </div>
              <div>
                <label>Description</label>
                <textarea
                  value={description}
                  onChange={(e) => {
                    setDescription(e.target.value);
                  }}
                />
              </div>
              <button className={classes.add} onClick={addRequest}>
                <img src={Add} alt="add" />
                Add
              </button>
            </div>
          </div>
          {requestsNum !== 0 && (
            <div className={classes.collaborations}>
              <h3>Collaborators Table</h3>
              <div className={classes.collaborationData}>
                <div className={classes.collaborationsList}>
                  {requests.map((item, index) => (
                    <CollaborationRequestElement
                      key={index}
                      uuid={item.uuid}
                      amount={index + 1}
                      token={token}
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
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default CollaborationRequest;
