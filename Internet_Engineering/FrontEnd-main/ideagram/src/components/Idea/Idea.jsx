import React from "react";
import classes from "./Idea.module.scss";
import IdeaIMG from "../../images/idea.jpg";
import { ThumbUp, Message } from "@mui/icons-material";
import Eye from "../../images/Eye.png";
import Delete from "../../images/delete.png";
import Edit from "../../images/edit2.png";
import { Link } from "react-router-dom";
import axios from "axios";
import { useDispatch } from "react-redux";
import { ideasActions } from "../../store/idea";

const Idea = ({
  type,
  uuid,
  token,
  title,
  image,
  goal,
  details,
  likes,
  views,
  comments,
  isShowLikes = true,
  isShowComments = true,
  isShowViews = true,
}) => {
  const dispatch = useDispatch();

  const manageDelete = async () => {
    try {
      await axios.delete(
        `${process.env.REACT_APP_API_ADDRESS}idea/detail/${uuid}`,
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );

      dispatch(
        ideasActions.deleteIdea({
          uuid: uuid,
        })
      );
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.ideaInfo}>
        <div className={classes.ideaTitle}>
          <h1 className={classes.title}>{title}</h1>
          {type === "MyIdeas" && (
            <Link
              className={`${classes.options} ${classes.editIdea}`}
              to={`/ideaStructure/editIdea/${uuid}`}
            >
              <img src={Edit} alt="Edit_Idea" />
              Edit
            </Link>
          )}
        </div>
        <div className={classes.ideaGoal}>
          <p>{goal}</p>
          {type === "MyIdeas" && (
            <button className={classes.deleteIdea} onClick={manageDelete}>
              <img src={Delete} alt="Delete_Idea" />
              Delete
            </button>
          )}
        </div>
        <div>
          <p className={classes.ideaDesc}>{details}</p>
        </div>
        <div className={classes.feedback}>
          {isShowLikes && (
            <div>
              <ThumbUp className={classes.icon} />
              {likes}
            </div>
          )}
          {isShowViews && (
            <div>
              <img className={classes.icon} src={Eye} alt="Views" />
              {views}
            </div>
          )}
          {isShowComments && (
            <div>
              <Message className={classes.icon} />
              {comments}
            </div>
          )}
        </div>
      </div>
      <Link to={`/stepsStructure/ideaShow/${uuid}`}>
        <img
          className={classes.ideaImage}
          src={
            image != null ? `http://api.iwantnet.space:8001${image}` : IdeaIMG
          }
          alt="Idea_Image"
        />
      </Link>
    </div>
  );
};

export default Idea;
