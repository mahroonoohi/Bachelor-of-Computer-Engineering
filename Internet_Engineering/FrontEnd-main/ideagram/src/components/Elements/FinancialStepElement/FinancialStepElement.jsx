import React from "react";
import classes from "./FinancialStepElement.module.scss";
import Edit from "../../../images/edit.png";
import Delete from "../../../images/delete2.png";
import { useDispatch } from "react-redux";
import axios from "axios";
import { financialStepsActions } from "../../../store/financialStep";

const FinancialStepElement = ({
  uuid,
  token,
  step,
  finishDate,
  priority,
  description,
  setStep,
  setFinishDate,
  setDescription,
  setPriority,
}) => {
  const dispatch = useDispatch();

  const deleteStepHandler = async () => {
    await axios.delete(
      `${process.env.REACT_APP_API_ADDRESS}idea/financial/detail/${uuid}`,
      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    dispatch(
      financialStepsActions.deleteFinancialStep({
        uuid: uuid,
      })
    );
  };

  const manageEdit = async () => {
    await deleteStepHandler();
    setStep(step);
    setFinishDate(finishDate);
    setDescription(description);
    setPriority(priority);
  };

  return (
    <div className={classes.container}>
      <p>{priority}</p>
      <h4>{step}</h4>
      <button onClick={manageEdit}>
        <img src={Edit} alt="Edit" />
      </button>
      <button onClick={deleteStepHandler}>
        <img src={Delete} alt="Delete" />
      </button>
    </div>
  );
};

export default FinancialStepElement;
