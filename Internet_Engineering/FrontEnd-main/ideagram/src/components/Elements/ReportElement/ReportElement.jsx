import React from "react";
import classes from "./ReportElement.module.scss";
import Edit from "../../../images/edit.png";
import Delete from "../../../images/delete2.png";
import { useDispatch } from "react-redux";
import { reportsActions } from "../../../store/report";

const ReportElement = ({
  amount,
  title,
  details,
  manageTitle,
  manageDetails,
}) => {
  const dispatch = useDispatch();

  const deleteReportHandler = () => {
    dispatch(
      reportsActions.deleteReport({
        title: title,
      })
    );
  };

  const editReportHandler = () => {
    manageTitle(title);
    manageDetails(details);

    dispatch(
      reportsActions.deleteReport({
        title: title,
      })
    );
  };

  return (
    <div className={classes.container}>
      <p>{amount}</p>
      <h4>{title}</h4>
      <button onClick={editReportHandler}>
        <img src={Edit} alt="Edit" />
      </button>
      <button onClick={deleteReportHandler}>
        <img src={Delete} alt="Delete" />
      </button>
    </div>
  );
};

export default ReportElement;
