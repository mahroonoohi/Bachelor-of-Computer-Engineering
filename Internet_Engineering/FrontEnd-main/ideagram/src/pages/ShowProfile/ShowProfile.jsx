import { React, useEffect, useState } from "react";
import classes from "./ShowProfile.module.scss";
import ProfileIMG from "../../images/user (2).png";
import FollowersIcon from "../../images/Multiple users silhouette.png";
import FollowingsIcon from "../../images/Subscriber.png";
import IdeaIcon from "../../images/IdeaIcon.png";
import FollowIcon from "../../images/Follow.png";
import ReportIcon from "../../images/Report.png";
import FollowersWhiteIcon from "../../images/FollowersWhite.png";
import FollowingsWhiteIcon from "../../images/FollowingsWhite.png";
import IdeaWhiteIcon from "../../images/IdeaWhite.png";
import { useParams, Link } from "react-router-dom";
import axios from "axios";
import { Idea, Skeleton, UserAccount } from "../../components";
import Menu from "../../images/filter (3).png";
import { UserFeedbackSmallMenu } from "../../components/SmallMenus";
import { Message } from "@mui/icons-material";

const ShowProfile = ({ token }) => {
  const params = useParams();
  const userId = params.userId;

  const [isLoading, setIsLoading] = useState(true);

  const [userProfileImage, setUserProfileImage] = useState(null);
  const [userUserName, setUserUsername] = useState("");
  const [userBio, setUserBio] = useState("");
  const [userFollowerCount, setUserFollowerCount] = useState(0);
  const [userFollowingCount, setUserFollowingCount] = useState(0);
  const [userIdeaCount, setUserIdeaCount] = useState(0);

  const [showFollowers, setShowFollowers] = useState(false);
  const [showFollowings, setShowFollowings] = useState(false);
  const [showIdeas, setShowIdeas] = useState(true);

  const [userIdeas, setUserIdeas] = useState([]);
  const [userFollowers, setUserFollowers] = useState([]);
  const [userFollowings, setUserFollowings] = useState([]);

  const [isShowMenu, setIsShowMenu] = useState(false);
  const [isFollowed, setIsFollowed] = useState(false);

  const showMenuHandler = (option) => {
    setIsShowMenu(!isShowMenu);
    option === "ideas" && manageShowIdeas();
    option === "followers" && manageShowFollowers();
    option === "followings" && manageShowFollowings();
  };

  useEffect(() => {
    const getUserData = async () => {
      try {
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
        setUserBio(res.data.bio);
        setUserFollowerCount(res.data.follower_count);
        setUserFollowingCount(res.data.following_count);
        setUserIdeaCount(res.data.idea_count);

        console.log(res.data.username);

        const isFollowedRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/is-follow-profile/${res.data.username}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(isFollowedRes);
        setIsFollowed(isFollowedRes.data.is_followed);

        const ideaRes = await axios.post(
          `${process.env.REACT_APP_API_ADDRESS}idea/filter/`,
          { usernames: [res.data.username] },
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(ideaRes.data);
        setUserIdeas(ideaRes.data);
        setUserIdeaCount(ideaRes.data.length);

        const followerRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/followers/${res.data.username}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(followerRes.data);
        setUserFollowers(followerRes.data);
        setUserFollowerCount(followerRes.data.length);

        const followingRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/followings/${res.data.username}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(followingRes.data);
        setUserFollowings(followingRes.data);
        setUserFollowingCount(followingRes.data.length);

        setIsLoading(false);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const manageFollow = async () => {
    try {
      await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}user/follow-profile/${userUserName}`,
        {},
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      setIsFollowed(!isFollowed);
    } catch (err) {
      console.log(err);
    }
  };

  const manageShowIdeas = () => {
    setShowIdeas(true);
    setShowFollowers(false);
    setShowFollowings(false);
  };

  const manageShowFollowers = () => {
    setShowIdeas(false);
    setShowFollowers(true);
    setShowFollowings(false);
  };

  const manageShowFollowings = () => {
    setShowIdeas(false);
    setShowFollowers(false);
    setShowFollowings(true);
  };

  return (
    <div className={classes.container}>
      <div className={classes.profileInfo}>
        <div className={classes.userInfoContainer}>
          <div className={classes.userInfo}>
            <img
              className={classes.profileImg}
              src={
                userProfileImage !== null
                  ? `http://api.iwantnet.space:8001${userProfileImage}`
                  : ProfileIMG
              }
              alt="Profile_Image"
            />
            <div className={classes.desc}>
              <h1>{userUserName}</h1>
              <p>{userBio}</p>
            </div>
          </div>
          <div className={classes.userFeedback}>
            <div>
              <img src={FollowersIcon} alt="Followers" />
              <h5>Followers</h5>
              <p>{userFollowerCount}</p>
            </div>
            <div>
              <img src={FollowingsIcon} alt="Followings" />
              <h5>Followings</h5>
              <p>{userFollowingCount}</p>
            </div>
            <div>
              <img src={IdeaIcon} alt="Idea" />
              <h5>Idea</h5>
              <p>{userIdeaCount}</p>
            </div>
          </div>
        </div>
        <div className={classes.options}>
          <button className={classes.followUserOption} onClick={manageFollow}>
            <img src={FollowIcon} alt="follow" />
            {isFollowed ? "Un Follow" : "Follow"}
          </button>
          <Link to={`/accountReport/${userUserName}`}>
            <button className={classes.reportUserOption}>
              <img src={ReportIcon} alt="report" />
              Report
            </button>
          </Link>
          <Link
            to={`http://api.iwantnet.space:8001/chat/chatpage/${userUserName}/${token}`}
            target="_blank"
            rel="noopener noreferrer"
          >
            <button className={classes.sendPersonalMessage}>
              <Message />
              Message
            </button>
          </Link>
        </div>
      </div>
      <div className={classes.userFeedbackOptions}>
        <button onClick={manageShowIdeas}>
          <img src={IdeaWhiteIcon} alt="Ideas" />
          Ideas
        </button>
        <button onClick={manageShowFollowers}>
          <img src={FollowersWhiteIcon} alt="Followers" />
          Followers
        </button>
        <button onClick={manageShowFollowings}>
          <img src={FollowingsWhiteIcon} alt="Followings" />
          Followings
        </button>
      </div>

      <div className={classes.smallMenu}>
        <button className={classes.showMenuBTN} onClick={showMenuHandler}>
          <img src={Menu} alt="menu" />
        </button>

        <UserFeedbackSmallMenu
          showMenuHandler={showMenuHandler}
          isShowMenu={isShowMenu}
        />
      </div>
      <div className={classes.userIdeas}>
        {isLoading ? (
          <Skeleton type="Idea" />
        ) : (
          showIdeas &&
          userIdeas.map((item, index) => (
            <Idea
              type="ShowProfile"
              key={index}
              uuid={item.uuid}
              token={token}
              image={item.image}
              title={item.title}
              goal={item.goal}
              details={item.details}
              likes={item.likes}
              views={item.views}
              comments={item.comments}
              isShowLikes={item.likes_count === null ? false : true}
              isComments={item.comments_count === null ? false : true}
              isShowViews={item.views_count === null ? false : true}
            />
          ))
        )}

        {showFollowers &&
          userFollowers.map((item, index) => (
            <UserAccount
              key={index}
              profileImage={item.profile_image}
              name={item.username}
              followers={item.followers}
              followings={item.followings}
              ideas={item.ideas}
            />
          ))}

        {showFollowings &&
          userFollowings.map((item, index) => (
            <UserAccount
              key={index}
              profileImage={item.profile_image}
              name={item.username}
              followers={item.followers}
              followings={item.followings}
              ideas={item.ideas}
            />
          ))}
      </div>
    </div>
  );
};

export default ShowProfile;
