import React from "react";
import classes from "./StepsStructureSmallMenu.module.scss";
import { Link, useLocation } from "react-router-dom";

const StepsStructureSmallMenu = ({ showMenuHandler, isShowMenu }) => {
  const location = useLocation();
  const uuid = location.pathname.split("/")[3];

  return (
    <ul
      className={`${classes.menu} ${
        isShowMenu ? classes.visible : classes.invisible
      }`}
    >
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to={`/stepsStructure/ideaShow/${uuid}`}
        >
          Idea
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to={`/stepsStructure/collaborationRequestShow/${uuid}`}
        >
          Collaboration Request
        </Link>
      </li>
      <li onClick={showMenuHandler}>
        <Link
          className={classes.sidebarOptions}
          to={`/stepsStructure/financialStepShow/${uuid}`}
        >
          Financial Step
        </Link>
      </li>
    </ul>
  );
};

export default StepsStructureSmallMenu;
