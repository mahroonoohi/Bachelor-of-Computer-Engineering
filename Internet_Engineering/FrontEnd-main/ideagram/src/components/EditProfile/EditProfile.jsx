import { React, useState, useEffect } from "react";
import classes from "./EditProfile.module.scss";
import UserProfile from "../../images/user (2).png";
import Apply from "../../images/apply.png";
import Next from "../../images/next.png";
import Previous from "../../images/prev.png";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import DatePicker from "react-datepicker";
import "react-datepicker/dist/react-datepicker.css";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { userMediaLinksActions } from "../../store/userMediaLink";
import UserMediaLinkElement from "../Elements/UserMediaLinkElement/UserMediaLinkElement";

const steps = ["1.Personal Information", "2.Change Password", "3.Manage Links"];

const EditProfile = ({ token }) => {
  const [mainUserName, setMainUserName] = useState("");
  const [selectedProfile, setUserSelectedProfile] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [userFirstName, setUserFirstName] = useState(null);
  const [userLastName, setUserLastName] = useState(null);
  const [userGender, setUserGender] = useState("male");
  const [userIsPublic, setUserIsPublic] = useState(false);
  const [userBirthDate, setUserBirthDate] = useState("2000-01-01");
  const [userCountry, setUserCountry] = useState(null);
  const [userState, setUserState] = useState(null);
  const [userCity, setUserCity] = useState(null);
  const [userAddress, setUserAddress] = useState(null);
  const [userUserName, setUserUserName] = useState(null);
  const [userBio, setUserBio] = useState(null);

  const dispatch = useDispatch();
  const userLinks = useSelector((state) => state.userMediaLink.userMediaLinks);
  const userLinksNum = useSelector(
    (state) => state.userMediaLink.userMediaLinksNum
  );

  const [userMediaLinkTitle, setUserMediaLinkTitle] = useState("github");
  const [userMediaLinkDetails, setUserMediaLinkDetails] = useState("");

  const [activeStep, setActiveStep] = useState(0);

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
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
        res.data.profile_image !== null &&
          setUserProfile(
            `http://api.iwantnet.space:8001${res.data.profile_image}`
          );
        setUserFirstName(res.data.first_name);
        setUserLastName(res.data.last_name);
        res.data.gender !== "other" && setUserGender(res.data.gender);
        setUserBio(res.data.bio);
        res.data.birth_date !== null && setUserBirthDate(res.data.birth_date);
        if (res.data.address !== null) {
          setUserCountry(res.data.address.country);
          setUserState(res.data.address.state);
          setUserCity(res.data.address.city);
          setUserAddress(res.data.address.address);
        }
        setUserUserName(res.data.username);
        setMainUserName(res.data.username);
        setUserIsPublic(res.data.is_public);

        const linksRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/social-media/`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        dispatch(userMediaLinksActions.deleteAll());
        console.log(linksRes);
        const links = linksRes.data;
        for (const item of links) {
          dispatch(
            userMediaLinksActions.addUserMediaLink({
              uuid: item.uuid,
              title: item.type,
              details: item.link,
            })
          );
        }
        console.log(userLinks);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const changeUserInfo = async () => {
    const formData = new FormData();
    if (userUserName !== mainUserName) {
      formData.append("username", userUserName);
    }
    formData.append("first_name", userFirstName);
    formData.append("last_name", userLastName);
    formData.append("birth_date", userBirthDate);
    formData.append("gender", userGender);
    formData.append("is_public", userIsPublic);
    console.log(userCountry);
    if (selectedProfile !== null) {
      formData.append("profile_image", selectedProfile);
    }

    for (const value of formData.values()) {
      console.log(value);
    }

    const userFullAddress = {
      country: userCountry,
      state: userState,
      city: userCity,
      address: userAddress,
    };

    await uploadNewUserData(formData, userFullAddress);
  };

  const changeBioInfo = async () => {
    const formData = new FormData();
    formData.append("bio", userBio);

    for (const value of formData.values()) {
      console.log(value);
    }

    await uploadNewUserBio(formData);
  };

  const uploadNewUserBio = async (formData) => {
    try {
      const res = await axios.put(
        `${process.env.REACT_APP_API_ADDRESS}user/profile/`,
        formData,
        {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(res);
    } catch (err) {
      console.log(err);
    }
  };

  const uploadNewUserData = async (formData, userFullAddress) => {
    try {
      const res = await axios.put(
        `${process.env.REACT_APP_API_ADDRESS}user/profile/`,
        formData,
        {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(res);

      const result = await axios.put(
        `${process.env.REACT_APP_API_ADDRESS}user/profile/`,
        { address: userFullAddress },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log(result);
    } catch (err) {
      console.log(err);
    }
  };

  const addUserSocialLinks = async () => {
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}user/social-media/`,
        {
          type: userMediaLinkTitle,
          link: userMediaLinkDetails,
        },
        {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(res);
      dispatch(
        userMediaLinksActions.addUserMediaLink({
          uuid: res.data.uuid,
          title: res.data.type,
          details: res.data.link,
        })
      );
    } catch (err) {
      console.log(err);
    }
  };

  const handleUploadedImage = (e) => {
    console.log(e.target.files[0]);
    setUserSelectedProfile(e.target.files[0]);
    setUserProfile(URL.createObjectURL(e.target.files[0]));
  };

  const addMediaLinkHandler = async () => {
    if (userMediaLinkTitle !== "" && userMediaLinkDetails !== "") {
      await addUserSocialLinks();

      setUserMediaLinkTitle("github");
      setUserMediaLinkDetails("");
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.body}>
        <h2>Edit Profile</h2>
        <div className={classes.steps}>
          <Stepper className={classes.stepper} activeStep={activeStep}>
            {steps.map((label, index) => {
              const stepProps = {};
              const labelProps = {};
              return (
                <Step key={label} {...stepProps}>
                  <StepLabel {...labelProps}>{label}</StepLabel>
                </Step>
              );
            })}
          </Stepper>
        </div>

        <div className={classes.profileInfo}>
          {activeStep === 0 && (
            <div className={classes.userInfo}>
              <div className={classes.info}>
                <div className={classes.profileImage}>
                  <input
                    id="selectProfileImage"
                    type="file"
                    accept="image/*"
                    onChange={(e) => {
                      handleUploadedImage(e);
                    }}
                  />
                  <label for="selectProfileImage">
                    <img
                      src={userProfile == null ? UserProfile : userProfile}
                      alt="User_Profile"
                    />
                  </label>
                </div>
                <div className={classes.userPersonalInfo}>
                  <div className={classes.enterInfo}>
                    <label>First Name</label>
                    <input
                      type="text"
                      value={userFirstName}
                      onChange={(e) => {
                        setUserFirstName(e.target.value);
                      }}
                    />
                  </div>
                  <div className={classes.enterInfo}>
                    <label>Last Name</label>
                    <input
                      type="text"
                      value={userLastName}
                      onChange={(e) => {
                        setUserLastName(e.target.value);
                      }}
                    />
                  </div>
                  <div className={classes.sideBySide}>
                    <div className={classes.enterGender}>
                      <label>Gender</label>
                      <select
                        name="gender"
                        onChange={(e) => {
                          setUserGender(e.target.value);
                        }}
                      >
                        {userGender === "male" && (
                          <>
                            <option value="male" selected>
                              Male
                            </option>
                            <option value="female">Female</option>
                          </>
                        )}
                        {userGender === "female" && (
                          <>
                            <option value="male">Male</option>
                            <option value="female" selected>
                              Female
                            </option>
                          </>
                        )}
                      </select>
                    </div>
                    <div className={classes.enterBirthDate}>
                      <label>Birth Date</label>
                      <DatePicker
                        selected={new Date(userBirthDate)}
                        onChange={(date) =>
                          setUserBirthDate(
                            `${date.getFullYear()}-${
                              date.getMonth() + 1
                            }-${date.getDate()}`
                          )
                        }
                        minDate={new Date("1923-01-01")}
                        maxDate={new Date()}
                        dateFormat="yyyy-MM-dd"
                      />
                    </div>
                  </div>
                  <div className={classes.enterAddress}>
                    <div>
                      <label>Country</label>
                      <input
                        type="text"
                        value={userCountry}
                        onChange={(e) => {
                          setUserCountry(e.target.value);
                        }}
                      />
                    </div>
                    <div>
                      <label>State</label>
                      <input
                        type="text"
                        value={userState}
                        onChange={(e) => {
                          setUserState(e.target.value);
                        }}
                      />
                    </div>
                    <div>
                      <label>City</label>
                      <input
                        type="text"
                        value={userCity}
                        onChange={(e) => {
                          setUserCity(e.target.value);
                        }}
                      />
                    </div>
                  </div>
                  <div className={classes.enterInfo}>
                    <label>Address</label>
                    <input
                      type="text"
                      value={userAddress}
                      onChange={(e) => {
                        setUserAddress(e.target.value);
                      }}
                    />
                  </div>
                  <div className={classes.enterInfo}>
                    <label>Username</label>
                    <input
                      type="text"
                      value={userUserName}
                      onChange={(e) => {
                        setUserUserName(e.target.value);
                      }}
                    />
                  </div>
                  <div className={classes.setUserStatus}>
                    <p>Status</p>

                    <label for="setUserPrivate" className={classes.filter}>
                      Private
                      <input
                        type="radio"
                        id="setUserPrivate"
                        name="Status"
                        checked={!userIsPublic}
                        onClick={() => {
                          setUserIsPublic(false);
                        }}
                      />
                      <span className={classes.custom}></span>
                    </label>

                    <label for="setUserPublic" className={classes.filter}>
                      Public
                      <input
                        type="radio"
                        id="setUserPublic"
                        name="Status"
                        checked={userIsPublic}
                        onClick={() => {
                          setUserIsPublic(true);
                        }}
                      />
                      <span className={classes.custom}></span>
                    </label>
                  </div>
                </div>
              </div>

              <div className={classes.options}>
                <button onClick={changeUserInfo}>
                  <img src={Apply} alt="apply" />
                  Apply
                </button>
                <button onClick={handleNext}>
                  <img src={Next} alt="next" />
                  Next
                </button>
              </div>
            </div>
          )}

          {activeStep === 1 && (
            <div className={classes.userBioInfo}>
              <div className={classes.bio}>
                <label>Bio</label>
                <textarea
                  type="text"
                  value={userBio}
                  onChange={(e) => {
                    setUserBio(e.target.value);
                  }}
                />
              </div>

              <div className={classes.options}>
                <button onClick={handleBack}>
                  <img src={Previous} alt="previous" />
                  Previous
                </button>
                <button onClick={changeBioInfo}>
                  <img src={Apply} alt="apply" />
                  Apply
                </button>
                <button onClick={handleNext}>
                  <img src={Next} alt="next" />
                  Next
                </button>
              </div>
            </div>
          )}

          {activeStep === 2 && (
            <div className={classes.userLinksInfo}>
              <div className={classes.addLinks}>
                <h3>Add Link</h3>
                <div className={classes.enterInfo}>
                  <div className={classes.enterSite}>
                    <label>Site</label>
                    <select
                      value={userMediaLinkTitle}
                      onChange={(e) => {
                        setUserMediaLinkTitle(e.target.value);
                      }}
                    >
                      <option value="github">Github</option>
                      <option value="gitlab">Gitlab</option>
                      <option value="telegram">Telegram</option>
                      <option value="linkedin">Linkedin</option>
                      <option value="instagram">Instagram</option>
                      <option value="facebook">Facebook</option>
                      <option value="twitter">Twitter</option>
                    </select>
                  </div>
                  <div className={classes.enterLink}>
                    <label>Link</label>
                    <input
                      type="text"
                      value={userMediaLinkDetails}
                      onChange={(e) => {
                        setUserMediaLinkDetails(e.target.value);
                      }}
                    />
                  </div>
                  <div className={classes.options}>
                    <button onClick={addMediaLinkHandler}>Add</button>
                  </div>
                </div>
              </div>
              <div className={classes.linksContainer}>
                <h3>Links</h3>
                <div className={classes.links}>
                  {userLinksNum !== 0 ? (
                    userLinks.map((item, index) => (
                      <UserMediaLinkElement
                        key={item.id}
                        uuid={item.uuid}
                        amount={index + 1}
                        title={item.title}
                        details={item.details}
                        token={token}
                      />
                    ))
                  ) : (
                    <p className={classes.noReport}>No Links Here</p>
                  )}
                </div>
              </div>
              <div className={classes.options}>
                <button onClick={handleBack}>
                  <img src={Previous} alt="previous" />
                  Previous
                </button>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default EditProfile;
