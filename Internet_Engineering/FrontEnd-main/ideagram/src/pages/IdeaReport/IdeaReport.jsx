import { React, useEffect } from "react";
import { Idea, UserAccount } from "../../components";
import ReportElement from "../../components/Elements/ReportElement/ReportElement";
import classes from "./IdeaReport.module.scss";
import Add from "../../images/add.png";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { reportsActions } from "../../store/report";
import { useParams } from "react-router-dom";
import axios from "axios";
import Apply from "../../images/apply.png";
import Cancel from "../../images/cross.png";
import IdeaImage from "../../images/idea.jpg";

const AccountReport = ({ token }) => {
  const params = useParams();
  const ideaId = params.ideaId;

  const dispatch = useDispatch();
  const reports = useSelector((state) => state.report.reports);
  const reportsNum = useSelector((state) => state.report.reportsNum);

  const [titleData, setTitleData] = useState("spam");
  const [detailsData, setDetailsData] = useState("");

  const [ideaImage, setIdeaImage] = useState(null);
  const [ideaTitle, setIdeaTitle] = useState("");
  const [ideaGoal, setIdeaGoal] = useState("");
  const [ideaAbstraction, setIdeaAbstraction] = useState("");

  useEffect(() => {
    const getUserData = async () => {
      try {
        dispatch(reportsActions.deleteAllReports());
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/detail/${ideaId}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        res.data.image !== null &&
          setIdeaImage(`http://api.iwantnet.space:8001${res.data.image}`);
        setIdeaTitle(res.data.title);
        setIdeaGoal(res.data.goal);
        setIdeaAbstraction(res.data.abstract);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const addReportHandler = async () => {
    if (titleData !== "" && detailsData !== "") {
      dispatch(
        reportsActions.addReport({
          id: titleData.replaceAll(/\s/g, ""),
          title: titleData,
          details: detailsData,
        })
      );

      setTitleData("");
      setDetailsData("");
    } else {
      alert("Fill data properly");
    }
  };

  const cancelAllReports = () => {
    dispatch(reportsActions.deleteAllReports());
  };

  const setAllReports = async () => {
    for (const report of reports) {
      try {
        await axios.post(
          `${process.env.REACT_APP_API_ADDRESS}report/idea/`,
          {
            idea: ideaId,
            report_reasons: report.title,
            description: report.details,
          },
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        dispatch(
          reportsActions.deleteReport({
            title: report.title,
          })
        );
      } catch (err) {
        console.log(err);
      }
    }
  };

  return (
    <div className={classes.container}>
      <h1>Idea Report</h1>
      <div className={classes.body}>
        <div className={classes.reportAccount}>
          <div className={classes.accountInfo}>
            <h3>Idea Information</h3>
            <div className={classes.details}>
              <img
                src={ideaImage === null ? IdeaImage : ideaImage}
                alt="Idea_Image"
              />
              <div>
                <h4>{ideaTitle}</h4>
                <h5>{ideaGoal}</h5>
                <p>{ideaAbstraction}</p>
              </div>
            </div>
          </div>
          <div className={classes.report}>
            <div>
              <label>Finish Data</label>

              <select
                name="status"
                onChange={(e) => {
                  setTitleData(e.target.value);
                }}
              >
                <option value="spam">Spam</option>
                <option value="promoting violence">Promoting Violence</option>
                <option value="encouragement to commit suicide">
                  Encouragement to commit suicide
                </option>
              </select>
            </div>
            <div>
              <label>Description</label>
              <textarea
                value={detailsData}
                cols={4}
                rows={3}
                onChange={(e) => {
                  setDetailsData(e.target.value);
                }}
              />
            </div>
            <div className={classes.addContainer}>
              <button className={classes.add} onClick={addReportHandler}>
                <img src={Add} alt="Add_Report" /> Add
              </button>
            </div>
          </div>
        </div>
        <div className={classes.reportsContainer}>
          <h1>Report Table</h1>
          <div className={classes.reports}>
            {reportsNum !== 0 ? (
              reports.map((item, index) => (
                <ReportElement
                  onClick={(e) => {
                    console.log(e);
                  }}
                  key={item.id}
                  id={item.id}
                  amount={index + 1}
                  title={item.title}
                  details={item.details}
                  manageTitle={setTitleData}
                  manageDetails={setDetailsData}
                />
              ))
            ) : (
              <p className={classes.noReport}>No Report Here</p>
            )}
          </div>
          <div className={classes.options}>
            <button className={classes.apply} onClick={setAllReports}>
              <img src={Apply} alt="apply" />
              Apply
            </button>
            <button className={classes.cancel} onClick={cancelAllReports}>
              <img src={Cancel} alt="cancel" />
              Cancel
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AccountReport;
