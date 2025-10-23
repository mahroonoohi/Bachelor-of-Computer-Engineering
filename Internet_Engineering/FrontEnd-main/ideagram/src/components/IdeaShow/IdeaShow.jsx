import { React, useEffect, useState } from "react";
import classes from "./IdeaShow.module.scss";
import ArtLabel from "../../images/ArtLabel.png";
import GamesLabel from "../../images/GamesLabel.png";
import DesignTechLabel from "../../images/DesignTechLabel.png";
import FoodCraftLabel from "../../images/FoodCraftLabel.png";
import FilmsLabel from "../../images/FilmsLabel.png";
import MusicLabel from "../../images/MusicLabel.png";
import PublishingLabel from "../../images/PublishingLabel.png";
import ScienceLabel from "../../images/ScienceLabel.png";
import IdeaImage from "../../images/idea.jpg";
import {
  Bookmark,
  BookmarkBorder,
  ThumbUp,
  Message,
  ThumbUpOffAlt,
} from "@mui/icons-material";
import Eye from "../../images/Eye.png";
import ReportIcon from "../../images/Report.png";
import NextIcon from "../../images/next.png";
import { UserAccount, UploadedFile } from "..";
import Comment from "../Comment/Comment";
import Profile from "../../images/profile.jpg";
import Send from "../../images/send.png";
import axios from "axios";
import { CircularProgress } from "@mui/material";
import { Link } from "react-router-dom";

const IdeaShow = ({ uuid, token }) => {
  const [ideaImage, setIdeaImage] = useState(null);
  const [ideaTitle, setIdeaTitle] = useState("");
  const [ideaGoal, setIdeaGoal] = useState("");
  const [ideaAbstraction, setIdeaAbstraction] = useState("");
  const [isArts, setIsArts] = useState(false);
  const [isGames, setIsGames] = useState(false);
  const [isDesignTech, setIsDesignTech] = useState(false);
  const [isFoodCraft, setIsFoodCraft] = useState(false);
  const [isFilms, setIsFilms] = useState(false);
  const [isMusics, setIsMusics] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [isScience, setIsScience] = useState(false);
  const [showLikes, setShowLikes] = useState(false);
  const [showViews, setShowViews] = useState(false);
  const [showComments, setShowComments] = useState(false);
  const [likesCount, setLikesCount] = useState(null);
  const [viewsCount, setViewsCount] = useState(null);
  const [commentsCount, setCommentsCount] = useState(null);
  const [ideaDescription, setIdeaDescription] = useState("");
  const [ideaComment, setIdeaComment] = useState("");
  const [ideaCommentsList, setIdeaCommentsList] = useState([]);
  const [ideaAttachedFilesList, setIdeaAttachedFilesList] = useState([]);

  const [userProfile, setUserProfile] = useState(null);
  const [userUsername, setUserUsername] = useState(null);
  const [userFollowers, setUserFollowers] = useState(null);
  const [userFollowings, setUserFollowings] = useState(null);
  const [userIdeas, setUserIdeas] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const [isSave, setIsSave] = useState(false);
  const [isLike, setIsLike] = useState(false);

  useEffect(() => {
    const getIdeaData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/detail/${uuid}`,
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
        setIsArts(res.data.classification.includes("art"));
        setIsGames(res.data.classification.includes("games"));
        setIsScience(res.data.classification.includes("science"));
        setIsPublishing(res.data.classification.includes("publishing"));
        setIsFilms(res.data.classification.includes("films"));
        setIsFoodCraft(res.data.classification.includes("food-craft"));
        setIsDesignTech(res.data.classification.includes("tech"));
        setIsMusics(res.data.classification.includes("music"));
        setShowLikes(res.data.show_likes);
        setShowViews(res.data.show_views);
        setShowComments(res.data.show_comments);
        setLikesCount(res.data.likes_count);
        setViewsCount(res.data.views_count);
        setCommentsCount(res.data.comments_count);
        setIdeaDescription(res.data.description);

        setUserProfile(res.data.profile.profile_image);
        setUserUsername(res.data.profile.username);
        setUserFollowers(res.data.profile.follower_count);
        setUserFollowings(res.data.profile.following_count);
        setUserIdeas(res.data.profile.idea_count);

        try {
          const attachedFilesRes = await axios.get(
            `${process.env.REACT_APP_API_ADDRESS}idea/attachment/${uuid}`,
            {
              headers: {
                Authorization: "Bearer " + token,
              },
            }
          );
          console.log(attachedFilesRes);
          setIdeaAttachedFilesList(attachedFilesRes.data);
        } catch (err) {
          console.log(err);
        }

        try {
          const commentsRes = await axios.get(
            `${process.env.REACT_APP_API_ADDRESS}idea/comment/${uuid}`,
            {
              headers: {
                Authorization: "Bearer " + token,
              },
            }
          );
          console.log(commentsRes);
          setIdeaCommentsList(commentsRes.data);
        } catch (err) {
          console.log(err);
        }

        try {
          const isSaveRes = await axios.get(
            `${process.env.REACT_APP_API_ADDRESS}idea/is-save-idea/${uuid}`,
            {
              headers: {
                Authorization: "Bearer " + token,
              },
            }
          );
          console.log(isSaveRes);
          setIsSave(isSaveRes.data.is_saved);
        } catch (err) {
          console.log(err);
        }

        try {
          const isLikeRes = await axios.get(
            `${process.env.REACT_APP_API_ADDRESS}idea/is-like/${uuid}`,
            {
              headers: {
                Authorization: "Bearer " + token,
              },
            }
          );
          console.log(isLikeRes);
          setIsLike(isLikeRes.data.is_liked);
        } catch (err) {
          console.log(err);
        }

        setIsLoading(false);
      } catch (err) {
        setIsLoading(false);
        console.log(err);
      }
    };
    getIdeaData();
  }, []);

  const setComment = async () => {
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/comment/${uuid}`,
        {
          comment: ideaComment,
        },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log(res);
      setIdeaCommentsList([...ideaCommentsList, res.data]);
      setIdeaComment("");
    } catch (err) {
      console.log(err);
    }
  };

  const manageSave = async () => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/save-idea/${uuid}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );
      setIsSave(!isSave);
    } catch (err) {
      console.log(err);
    }
  };

  const manageLike = async () => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/like/${uuid}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        }
      );

      if (isLike) {
        setLikesCount(likesCount - 1);
      } else {
        setLikesCount(likesCount + 1);
      }
      setIsLike(!isLike);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className={classes.body}>
      <div className={classes.ideaData}>
        <div className={classes.ideaInfo}>
          <div className={classes.ideaDetails}>
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
            <div className={classes.options}>
              {isLoading && <CircularProgress />}
              <button onClick={manageSave}>
                {isSave ? (
                  <Bookmark className={classes.saveIdeaButton} />
                ) : (
                  <BookmarkBorder className={classes.saveIdeaButton} />
                )}
                Save
              </button>
              <Link to={`/ideaReport/${uuid}`}>
                <button className={classes.reportUserOption}>
                  <img src={ReportIcon} alt="report" />
                  Report
                </button>
              </Link>
            </div>
          </div>
          {(showLikes || showViews || showComments) && (
            <div className={classes.ideaFeedback}>
              {showLikes && (
                <div onClick={manageLike}>
                  {isLike ? (
                    <ThumbUpOffAlt
                      className={`${classes.icon} ${classes.likeIdea}`}
                    />
                  ) : (
                    <ThumbUp
                      className={`${classes.icon} ${classes.likeIdea}`}
                    />
                  )}
                  {likesCount}
                </div>
              )}
              {showViews && (
                <div>
                  <img className={classes.icon} src={Eye} alt="Views" />
                  {viewsCount}
                </div>
              )}
              {showComments && (
                <div>
                  <Message className={classes.icon} />
                  {commentsCount}
                </div>
              )}
            </div>
          )}
          {(isArts ||
            isGames ||
            isDesignTech ||
            isFoodCraft ||
            isFilms ||
            isMusics ||
            isPublishing ||
            isScience) && (
            <div className={classes.ideaLabels}>
              {isArts && (
                <div>
                  <img src={ArtLabel} alt="Art_Label" />
                  <p>Arts</p>
                </div>
              )}
              {isGames && (
                <div>
                  <img src={GamesLabel} alt="Games_Label" />
                  <p>Games</p>
                </div>
              )}
              {isDesignTech && (
                <div>
                  <img src={DesignTechLabel} alt="Tech_Label" />
                  <p>Tech</p>
                </div>
              )}
              {isFoodCraft && (
                <div>
                  <img src={FoodCraftLabel} alt="Food_Craft_Label" />
                  <p>Food & Craft</p>
                </div>
              )}
              {isFilms && (
                <div>
                  <img src={FilmsLabel} alt="Films_Label" />
                  <p>Films</p>
                </div>
              )}
              {isMusics && (
                <div>
                  <img src={MusicLabel} alt="Musics_Label" />
                  <p>Musics</p>
                </div>
              )}
              {isPublishing && (
                <div>
                  <img src={PublishingLabel} alt="Publishing_Label" />
                  <p>Publishing</p>
                </div>
              )}
              {isScience && (
                <div>
                  <img src={ScienceLabel} alt="Science_Label" />
                  <p>Science</p>
                </div>
              )}
            </div>
          )}
        </div>
        <div className={classes.userInfo}>
          <div className={classes.userDetails}>
            <h2>Creator</h2>
            <UserAccount
              profileImage={userProfile}
              name={userUsername}
              followers={userFollowers}
              followings={userFollowings}
              ideas={userIdeas}
            />
          </div>
          <div className={classes.supportIdea}>
            <h2>Support</h2>
            <p>
              Support the Idea for <b>NO reward</b>. Just because it speaks to
              you.
            </p>
            <div>
              <input type="text" />
              <button>
                <img src={NextIcon} alt="Next" />
              </button>
            </div>
          </div>
        </div>
      </div>
      <div className={classes.ideDescription}>
        <div className={classes.ideaDesc}>
          <h2>Description</h2>
          <p className={classes.desc}>{ideaDescription}</p>
        </div>
        <div className={classes.uploadedFiles}>
          <h2>Attached Files</h2>
          {isLoading ? (
            <CircularProgress />
          ) : ideaAttachedFilesList.length !== 0 ? (
            <div className={classes.uploadedFilesList}>
              {ideaAttachedFilesList.map((item, index) => (
                <UploadedFile
                  key={index}
                  token={token}
                  uuid={item.uuid}
                  type={item.file.split(".")[1]}
                  fileName={item.file}
                  downloadOrDelete="download"
                />
              ))}
            </div>
          ) : (
            <p className={classes.noFile}>No Attach File</p>
          )}
        </div>
      </div>
      <div>
        <div className={classes.comments}>
          <h2>Comments</h2>
          <div className={classes.commentsList}>
            {isLoading ? (
              <CircularProgress />
            ) : (
              ideaCommentsList.map((item, index) => (
                <Comment
                  key={index}
                  profile={item.profile.profile_image}
                  text={item.comment}
                />
              ))
            )}
          </div>
        </div>
        <div className={classes.ideaSupport}>
          <h2>Write Comment</h2>
          <div className={classes.support}>
            <input
              type="text"
              value={ideaComment}
              onChange={(e) => {
                setIdeaComment(e.target.value);
              }}
            />
            <button onClick={setComment}>
              <img src={Send} alt="send" />
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default IdeaShow;
