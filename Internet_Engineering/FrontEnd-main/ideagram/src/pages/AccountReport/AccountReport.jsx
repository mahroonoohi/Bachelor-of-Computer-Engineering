import { React, useEffect } from "react";
import { UserAccount } from "../../components";
import ReportElement from "../../components/Elements/ReportElement/ReportElement";
import classes from "./AccountReport.module.scss";
import Add from "../../images/add.png";
import { useState } from "react";
import { useDispatch, useSelector } from "react-redux";
import { reportsActions } from "../../store/report";
import { useParams } from "react-router-dom";
import axios from "axios";
import Apply from "../../images/apply.png";
import Cancel from "../../images/cross.png";

const AccountReport = ({ token }) => {
  const params = useParams();
  const userId = params.userId;

  const dispatch = useDispatch();
  const reports = useSelector((state) => state.report.reports);
  const reportsNum = useSelector((state) => state.report.reportsNum);

  const [titleData, setTitleData] = useState("spam");
  const [detailsData, setDetailsData] = useState("");

  const [userProfileImage, setUserProfileImage] = useState(null);
  const [userUserName, setUserUsername] = useState("");
  const [userFollowerCount, setUserFollowerCount] = useState(0);
  const [userFollowingCount, setUserFollowingCount] = useState(0);
  const [userIdeaCount, setUserIdeaCount] = useState(0);

  useEffect(() => {
    const getUserData = async () => {
      try {
        dispatch(reportsActions.deleteAllReports());
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/general/profile/${userId}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        setUserProfileImage(res.data.profile_image);
        setUserUsername(res.data.username);
        setUserFollowerCount(res.data.follower_count);
        setUserFollowingCount(res.data.following_count);
        setUserIdeaCount(res.data.idea_count);
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
          `${process.env.REACT_APP_API_ADDRESS}report/profile/`,
          {
            profile_username: userUserName,
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
      <h1>Account Report</h1>
      <div className={classes.body}>
        <div className={classes.reportAccount}>
          <div className={classes.accountInfo}>
            <h3>Account Information</h3>
            <UserAccount
              profileImage={userProfileImage}
              name={userUserName}
              followers={userFollowerCount}
              followings={userFollowingCount}
              ideas={userIdeaCount}
            />
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
