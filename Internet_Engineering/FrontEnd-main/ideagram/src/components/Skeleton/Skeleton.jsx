import React from "react";
import classes from "./Skeleton.module.scss";

export default function Skeleton({ type }) {
  const COUNTER = 6;
  const IdeaSkeleton = () => (
    <div className={classes.container}>
      <div className={classes.ideaInfo}>
        <div className={classes.ideaTitle}></div>
        <div className={classes.ideaGoal}></div>
        <div className={classes.ideaDesc}></div>
      </div>
      <div className={classes.ideaImage}></div>
    </div>
  );

  const ToolbarSkeleton = () => (
    <div className={classes.options}>
      <div className={classes.account}></div>
      <div className={classes.userImage}></div>
    </div>
  );

  if (type === "Idea") return Array(COUNTER).fill(<IdeaSkeleton />);
  if (type === "Toolbar") return <ToolbarSkeleton />;
}
