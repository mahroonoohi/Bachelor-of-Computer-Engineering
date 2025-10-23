import { React, useState, useEffect } from "react";
import classes from "./FinancialStep.module.scss";
import Add from "../../images/add.png";
import { useDispatch, useSelector } from "react-redux";
import { financialStepsActions } from "../../store/financialStep";
import axios from "axios";
import FinancialStepElement from "../Elements/FinancialStepElement/FinancialStepElement";

const FinancialStep = ({ uuid, token }) => {
  const dispatch = useDispatch();
  const financialSteps = useSelector(
    (state) => state.financialSteps.financialSteps
  );
  const financialStepsNum = useSelector(
    (state) => state.financialSteps.financialStepsNum
  );

  const [step, setStep] = useState("");
  const [priority, setPriority] = useState(1);
  const [cost, setCost] = useState(0);
  const [description, setDescription] = useState("");

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/financial/${uuid}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        dispatch(financialStepsActions.deleteAll());
        for (const req of res.data) {
          dispatch(
            financialStepsActions.addFinancialStep({
              uuid: req.uuid,
              step: req.title,
              priority: req.priority,
              cost: req.cost,
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

  const addStep = async () => {
    console.log("add");
    if (step !== "" && description !== "" && cost !== 0) {
      console.log("added");
      try {
        const res = await axios.post(
          `${process.env.REACT_APP_API_ADDRESS}idea/financial/${uuid}`,
          [
            {
              title: step,
              priority: priority,
              cost: cost,
              description: description,
              unit: "rial",
            },
          ],
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        dispatch(
          financialStepsActions.addFinancialStep({
            uuid: res.data[0].uuid,
            step: res.data[0].title,
            priority: res.data[0].priority,
            cost: res.data[0].cost,
            description: res.data[0].description,
          })
        );
        setStep("");
        setCost(0);
        setDescription("");
        setPriority(1);
      } catch (err) {
        console.log(err);
        alert("Please set distinct priorities");
      }
    } else {
      alert("Please fill the fields properly");
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.body}>
        <h2>
          Financial
          <br />
          Step
        </h2>
        <div className={classes.collaborationInfo}>
          <div className={classes.collaborationDetails}>
            <h3>Finance Information</h3>
            <div className={classes.details}>
              <div>
                <label>Step</label>
                <input
                  type="text"
                  value={step}
                  onChange={(e) => {
                    setStep(e.target.value);
                  }}
                />
              </div>
              <div className={classes.enterData}>
                <label>Priority</label>
                <input
                  type="number"
                  min={1}
                  className={classes.short}
                  value={priority}
                  onChange={(e) => {
                    setPriority(e.target.value);
                  }}
                />
              </div>
              <div>
                <label>Cost</label>
                <input
                  type="number"
                  min={1}
                  className={classes.short}
                  value={cost}
                  onChange={(e) => {
                    setCost(e.target.value);
                  }}
                />
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
              <button className={classes.add} onClick={addStep}>
                <img src={Add} alt="add" />
                Add
              </button>
            </div>
          </div>
          {financialStepsNum !== 0 && (
            <div className={classes.collaborations}>
              <h3>Finance Table</h3>
              <div className={classes.collaborationData}>
                <div className={classes.collaborationsList}>
                  {financialSteps.map((item, index) => (
                    <FinancialStepElement
                      key={index}
                      uuid={item.uuid}
                      token={token}
                      step={item.step}
                      priority={item.priority}
                      cost={item.cost}
                      description={item.description}
                      setStep={setStep}
                      setCost={setCost}
                      setDescription={setDescription}
                      setPriority={setPriority}
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

export default FinancialStep;
