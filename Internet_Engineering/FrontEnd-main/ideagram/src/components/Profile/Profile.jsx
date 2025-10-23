import { React, useEffect, useState } from "react";
import classes from "./Profile.module.scss";
import UserProfile from "../../images/user (2).png";
import Next from "../../images/next.png";
import Previous from "../../images/prev.png";
import axios from "axios";
import UserSocialMediaLink from "../UserSocialMediaLink/UserScocialMediaLink";
import { CircularProgress } from "@mui/material";

const Profile = ({ token }) => {
  const [nextPage, setNextPage] = useState("first");
  const [userProfile, setUserProfile] = useState(null);
  const [userFirstName, setUserFirstName] = useState(null);
  const [userLastName, setUserLastName] = useState(null);
  const [userGender, setUserGender] = useState(null);
  const [userBirthDate, setUserBirthDate] = useState(null);
  const [userCountry, setUserCountry] = useState(" ");
  const [userState, setUserState] = useState(" ");
  const [userCity, setUserCity] = useState(" ");
  const [userAddress, setUserAddress] = useState(" ");
  const [userUserName, setUserUserName] = useState(null);
  const [userBio, setUserBio] = useState(null);
  const [userIsPublic, setUserIsPublic] = useState(false);
  const [userIsBanned, setUserIsBanned] = useState(false);
  const [userIsActive, setUserIsActive] = useState(false);
  const [userLinksList, setUserLinksList] = useState([]);

  const [isLoading, setIsLoading] = useState(true);

  const handleNext = () => {
    setNextPage("sec");
  };

  const handlePrev = () => {
    setNextPage("first");
  };

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        setUserProfile(res.data.profile_image);
        setUserFirstName(res.data.first_name);
        setUserLastName(res.data.last_name);
        setUserGender(res.data.gender);
        setUserBio(res.data.bio);
        setUserBirthDate(res.data.birth_date);
        if (res.data.address !== null) {
          setUserCountry(res.data.address.country);
          setUserState(res.data.address.state);
          setUserCity(res.data.address.city);
          setUserAddress(res.data.address.address);
        }
        setUserUserName(res.data.username);
        setUserIsPublic(res.data.is_public);
        setUserIsActive(res.data.is_active);
        setUserIsBanned(res.data.is_banned);

        setIsLoading(false);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/social-media/`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        setUserLinksList(res.data);
        console.log(userLinksList);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  return (
    <div className={classes.body}>
      <h2>Profile</h2>
      <div className={classes.profileInfo}>
        {nextPage === "first" ? (
          <div className={classes.firstPageInfo}>
            <div className={classes.info}>
              <img
                src={
                  userProfile == null
                    ? UserProfile
                    : `http://api.iwantnet.space:8001${userProfile}`
                }
                alt="User_Profile"
                className={classes.profileImage}
              />
              <div className={classes.userPersonalInfo}>
                <div className={classes.enterInfo}>
                  <label>First Name</label>
                  <p>{userFirstName}</p>
                </div>
                <div className={classes.enterInfo}>
                  <label>Last Name</label>
                  <p>{userLastName}</p>
                </div>
                <div className={classes.sideBySide}>
                  <div className={classes.enterGender}>
                    <label>Gender</label>
                    <p>{userGender}</p>
                  </div>
                  <div className={classes.enterBirthDate}>
                    <label>Birth Date</label>
                    <p>{userBirthDate}</p>
                  </div>
                </div>
                <div className={classes.enterInfo}>
                  <label>Address</label>
                  {isLoading ? (
                    <CircularProgress />
                  ) : (
                    <textarea
                      rows={4}
                    >{`${userCountry}-${userState}-${userCity}-${userAddress}`}</textarea>
                  )}
                </div>
                <div className={classes.enterInfo}>
                  <label>Username</label>
                  <p>{userUserName}</p>
                </div>
              </div>
            </div>

            <div className={classes.options}>
              <button onClick={handleNext}>
                <img src={Next} alt="next" />
                Next
              </button>
            </div>
          </div>
        ) : (
          <div className={classes.secPageInfo}>
            <div className={classes.bio}>
              <label>Bio</label>
              <p>{userBio}</p>
            </div>
            <div className={classes.info}>
              <div>
                <label>Profile Status</label>
                <p>{userIsPublic ? "Public" : "Private"}</p>
              </div>
              <div>
                <label>Activation Status</label>
                <p>{userIsActive ? "Active" : "Inactive"}</p>
              </div>
              <div>
                <label>Ban Status</label>
                <p>{userIsBanned ? "Banned" : "Not Banned"}</p>
              </div>
            </div>
            <div className={classes.linksContainer}>
              <label>Links</label>
              <div className={classes.links}>
                {userLinksList.map((item) => (
                  <UserSocialMediaLink type={item.type} link={item.link} />
                ))}
              </div>
            </div>
            <div className={classes.options}>
              <button onClick={handlePrev}>
                <img src={Previous} alt="previous" />
                Previous
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default Profile;
