import { React, useEffect, useState } from "react";
import classes from "./FinancialStepShow.module.scss";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import { StepInfo } from "..";
import axios from "axios";

const FinancialStepShow = ({ token, uuid }) => {
  const [steps, setSteps] = useState([]);
  const [stepsInfo, setStepsInfo] = useState([]);
  const [activeStep, setActiveStep] = useState(null);
  const [stepInfo, setStepInfo] = useState({
    title: "",
    cost: "",
    description: "",
  });

  const manageStepsInfo = (index) => {
    setStepInfo(stepsInfo[index]);
    setActiveStep(index);
  };

  useEffect(() => {
    const getIdeaData = async () => {
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
        const stepsList = res.data;
        stepsList.sort((a, b) =>
          a.priority > b.priority ? 1 : b.priority > a.priority ? -1 : 0
        );
        const stepsNames = [];
        for (const item of stepsList) {
          stepsNames.push(item.title);
        }
        setSteps(stepsNames);
        setStepsInfo(stepsList);
      } catch (err) {
        console.log(err);
      }
    };
    getIdeaData();
  }, []);

  return (
    <div className={classes.body}>
      <h2>Financial Step</h2>
      <div className={classes.steps}>
        <h4>Steps</h4>
        <Stepper className={classes.stepper} activeStep={activeStep}>
          {steps.map((label, index) => {
            const stepProps = {};
            const labelProps = {};
            return (
              <Step key={label} {...stepProps}>
                <StepLabel
                  {...labelProps}
                  onClick={() => manageStepsInfo(index)}
                >
                  {label}
                </StepLabel>
              </Step>
            );
          })}
        </Stepper>
      </div>
      <div className={classes.stepsInfo}>
        <h4>
          Step
          <br />
          Information
        </h4>
        <div className={classes.stepInfo}>
          <StepInfo
            firstTitle="Step"
            secTitle="Cost"
            thirdTitle="Description"
            stepName={stepInfo.title}
            finishDate={stepInfo.cost}
            description={stepInfo.description}
          />
        </div>
      </div>
    </div>
  );
};

export default FinancialStepShow;
