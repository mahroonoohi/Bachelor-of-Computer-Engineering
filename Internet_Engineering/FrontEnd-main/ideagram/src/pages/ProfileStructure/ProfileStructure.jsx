import { React } from "react";
import classes from "./ProfileStructure.module.scss";
import MyProfile from "../../images/MyProfile.png";
import CreateIdeaIMG from "../../images/CreateIdea.png";
import My_Idea from "../../images/MyIdea.png";
import Saved_Ideas from "../../images/SavedIdeas.png";
import Follower from "../../images/Follower.png";
import Following from "../../images/Following.png";
import Edit_Profile from "../../images/EditProfile.png";
import { useLocation, Link } from "react-router-dom";
import {
  EditProfile,
  Followings,
  Followers,
  MyIdeas,
  Profile,
  SavedIdeas,
  CreateIdea,
} from "../../components";

const ProfileStructure = ({ token }) => {
  const location = useLocation();
  console.log(location.pathname);
  const url =
    location.pathname.split("/")[location.pathname.split("/").length - 1];

  return (
    <div className={classes.container}>
      <div className={classes.sidebar}>
        <Link className={classes.sidebarOptions} to="/profileStructure/profile">
          <img src={MyProfile} alt="Profile" /> Profile
        </Link>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/editProfile"
        >
          <img src={Edit_Profile} alt="Edit_Profile" /> Edit Profile
        </Link>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/createIdea"
        >
          <img src={CreateIdeaIMG} alt="Create_Idea" /> Create Idea
        </Link>
        <Link className={classes.sidebarOptions} to="/profileStructure/myIdeas">
          <img src={My_Idea} alt="My_Ideas" /> My Ideas
        </Link>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/savedIdeas"
        >
          <img src={Saved_Ideas} alt="Saved_Ideas" /> Saved Ideas
        </Link>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/followers"
        >
          <img src={Follower} alt="Follower" /> Followers
        </Link>
        <Link
          className={classes.sidebarOptions}
          to="/profileStructure/followings"
        >
          <img src={Following} alt="Following" /> Followings
        </Link>
      </div>
      <div className={classes.main}>
        {
          {
            profile: <Profile token={token} />,
            createIdea: <CreateIdea token={token} />,
            myIdeas: <MyIdeas token={token} />,
            savedIdeas: <SavedIdeas token={token} />,
            followers: <Followers token={token} />,
            followings: <Followings token={token} />,
            editProfile: <EditProfile token={token} />,
          }[url]
        }
      </div>
    </div>
  );
};

export default ProfileStructure;
