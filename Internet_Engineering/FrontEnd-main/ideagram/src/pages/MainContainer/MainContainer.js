import { React, useContext } from "react";
import classes from "./MainContainer.module.scss";
import { Header, Footer } from "../../components";
import { useLocation } from "react-router-dom";
import {
  MainPage,
  AccountReport,
  ProfileStructure,
  IdeaStructure,
  ShowProfile,
  StepsStructure,
  IdeaReport,
} from "../";
import AuthContext from "../../api/AuthContext";

const MainContainer = () => {
  const token = useContext(AuthContext).getAccessToken();
  console.log(token);

  const location = useLocation();
  console.log(location.pathname.split("/"));
  const url = location.pathname.split("/")[1];
  console.log(url);

  return (
    <div className={classes.container}>
      <Header />
      <div className={classes.body}>
        {
          {
            mainPage: <MainPage token={token} />,
            accountReport: <AccountReport token={token} />,
            ideaReport: <IdeaReport token={token} />,
            showProfile: <ShowProfile token={token} />,
            profileStructure: <ProfileStructure token={token} />,
            stepsStructure: <StepsStructure token={token} />,
            ideaStructure: <IdeaStructure token={token} />,
          }[url]
        }
      </div>
      <Footer />
    </div>
  );
};

export default MainContainer;
