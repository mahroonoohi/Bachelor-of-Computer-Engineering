import { React, useState, useEffect } from "react";
import classes from "./EditIdea.module.scss";
import Stepper from "@mui/material/Stepper";
import Step from "@mui/material/Step";
import StepLabel from "@mui/material/StepLabel";
import "react-datepicker/dist/react-datepicker.css";
import SelectImage from "../../images/selectImage.png";
import ArtLabel from "../../images/ArtLabel.png";
import GamesLabel from "../../images/GamesLabel.png";
import DesignTechLabel from "../../images/DesignTechLabel.png";
import FoodCraftLabel from "../../images/FoodCraftLabel.png";
import FilmsLabel from "../../images/FilmsLabel.png";
import MusicLabel from "../../images/MusicLabel.png";
import PublishingLabel from "../../images/PublishingLabel.png";
import ScienceLabel from "../../images/ScienceLabel.png";
import Next from "../../images/next.png";
import Apply from "../../images/apply.png";
import Previous from "../../images/prev.png";
import AttachFile from "../../images/attachFile.png";
import { UploadedFile } from "..";
import axios from "axios";
import { attachedFilesActions } from "../../store/attachedFilesForIdea";
import { useDispatch, useSelector } from "react-redux";
import { CircularProgress } from "@mui/material";

const steps = ["1.primary Information", "2.Description", "3.Attached Files"];

const CreateIdea = ({ uuid, token }) => {
  const dispatch = useDispatch();
  const attachedFiles = useSelector(
    (state) => state.attachedFiles.attachedFiles
  );
  const attachedFilesNum = useSelector(
    (state) => state.attachedFiles.attachedFilesNum
  );

  const [activeStep, setActiveStep] = useState(0);

  const [ideaImageDisplay, setIdeaImageDisplay] = useState(null);
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
  const [ideaDescription, setIdeaDescription] = useState("");

  const [isFileUploaded, setIsFileUploaded] = useState(true);

  useEffect(() => {
    const getUserData = async () => {
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
          setIdeaImageDisplay(
            `http://api.iwantnet.space:8001${res.data.image}`
          );
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
        setIdeaDescription(res.data.description);
      } catch (err) {
        console.log(err);
      }

      try {
        const attachmentRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/attachment/${uuid}`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(attachmentRes);
        attachedFilesActions.deleteAllAttachedFiles();
        for (const item of attachmentRes.data) {
          dispatch(
            attachedFilesActions.addAttachedFiles({
              uuid: item.uuid,
              name: item.file,
            })
          );
        }
      } catch (e) {
        console.log(e);
      }
    };
    getUserData();
  }, []);

  const setChangedData = async () => {
    const formData = new FormData();
    isFilms && formData.append("classification", "films");
    isScience && formData.append("classification", "science");
    isPublishing && formData.append("classification", "publishing");
    isMusics && formData.append("classification", "music");
    isGames && formData.append("classification", "games");
    isFoodCraft && formData.append("classification", "food-craft");
    isDesignTech && formData.append("classification", "tech");
    isArts && formData.append("classification", "art");
    formData.append("title", ideaTitle);
    formData.append("goal", ideaGoal);
    formData.append("abstract", ideaAbstraction);
    formData.append("description", ideaDescription);
    ideaImage !== null && formData.append("image", ideaImage);
    formData.append("show_likes", showLikes);
    formData.append("show_views", showViews);
    formData.append("show_comments", showComments);

    for (const value of formData.values()) {
      console.log(value);
    }

    await changeIdea(formData);
  };

  const changeIdea = async (formData) => {
    try {
      const res = await axios.put(
        `${process.env.REACT_APP_API_ADDRESS}idea/detail/${uuid}`,
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

  const uploadAttachFile = async (e) => {
    console.log(e.target.files[0]);
    const selectedFile = e.target.files[0];
    const formData = new FormData();
    formData.append("file", selectedFile);
    try {
      setIsFileUploaded(false);
      const res = await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/attachment/${uuid}`,
        formData,
        {
          headers: {
            Authorization: "Bearer " + token,
            "Content-Type": "multipart/form-data",
          },
        }
      );
      console.log(res);
      dispatch(
        attachedFilesActions.addAttachedFiles({
          uuid: res.data.uuid,
          name: selectedFile.name,
        })
      );
      setIsFileUploaded(true);
    } catch (e) {
      setIsFileUploaded(true);
      alert("Couldn't upload file");
      console.log(e);
    }
  };

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleUploadedFile = (e) => {
    console.log(e.target.files[0]);
    setIdeaImage(e.target.files[0]);
    setIdeaImageDisplay(URL.createObjectURL(e.target.files[0]));
  };

  return (
    <div className={classes.container}>
      <div className={classes.body}>
        <h2>Edit Idea</h2>
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

        {activeStep === 0 && (
          <div className={classes.newIdeaInfo}>
            <div className={classes.ideaDetails}>
              <div className={classes.selectIdeaImage}>
                <input
                  id="selectIdeaImage"
                  type="file"
                  accept="image/*"
                  onChange={(e) => {
                    handleUploadedFile(e);
                  }}
                />
                <label for="selectIdeaImage">
                  <img
                    src={
                      ideaImageDisplay === null ? SelectImage : ideaImageDisplay
                    }
                    alt="Select_Image"
                  />
                </label>
              </div>
              <div className={classes.enterIdeaDetails}>
                <div>
                  <label>Title</label>
                  <input
                    type="text"
                    value={ideaTitle}
                    onChange={(e) => {
                      setIdeaTitle(e.target.value);
                    }}
                  />
                </div>
                <div>
                  <label>Goals</label>
                  <input
                    type="text"
                    value={ideaGoal}
                    onChange={(e) => {
                      setIdeaGoal(e.target.value);
                    }}
                  />
                </div>
                <div>
                  <label>Abstract</label>
                  <textarea
                    value={ideaAbstraction}
                    onChange={(e) => {
                      setIdeaAbstraction(e.target.value);
                    }}
                  />
                </div>
              </div>
            </div>

            <div className={classes.newIdeaLabels}>
              <p>Labels</p>
              <div className={classes.labels}>
                <div>
                  <input
                    id="artLabel"
                    type="checkbox"
                    checked={isArts}
                    onChange={(e) => {
                      setIsArts(e.target.selected);
                    }}
                  />
                  <label for="artLabel">
                    <img src={ArtLabel} alt="Art" />
                    Arts
                  </label>
                </div>
                <div>
                  <input
                    type="checkbox"
                    id="gameLabel"
                    checked={isGames}
                    onChange={(e) => {
                      setIsGames(e.target.selected);
                    }}
                  />
                  <label for="gameLabel">
                    <img src={GamesLabel} alt="Games" />
                    Games
                  </label>
                </div>
                <div>
                  <input
                    id="designTechLabel"
                    type="checkbox"
                    checked={isDesignTech}
                    onChange={(e) => {
                      setIsDesignTech(e.target.selected);
                    }}
                  />
                  <label for="designTechLabel">
                    <img src={DesignTechLabel} alt="Design_Tech" />
                    Tech
                  </label>
                </div>
                <div>
                  <input
                    id="foodLabel"
                    type="checkbox"
                    checked={isFoodCraft}
                    onChange={(e) => {
                      setIsFoodCraft(e.target.selected);
                    }}
                  />
                  <label for="foodLabel">
                    <img src={FoodCraftLabel} alt="Food_Craft" />
                    Food & Craft
                  </label>
                </div>
                <div>
                  <input
                    id="filmLabel"
                    type="checkbox"
                    checked={isFilms}
                    onChange={(e) => {
                      setIsFilms(e.target.selected);
                    }}
                  />
                  <label for="filmLabel">
                    <img src={FilmsLabel} alt="Films" />
                    Films
                  </label>
                </div>
                <div>
                  <input
                    id="musicLabel"
                    type="checkbox"
                    checked={isMusics}
                    onChange={(e) => {
                      setIsMusics(e.target.selected);
                    }}
                  />
                  <label for="musicLabel">
                    <img src={MusicLabel} alt="Music" />
                    Music
                  </label>
                </div>
                <div>
                  <input
                    id="publishingLabel"
                    type="checkbox"
                    checked={isPublishing}
                    onChange={(e) => {
                      setIsPublishing(e.target.selected);
                    }}
                  />
                  <label for="publishingLabel">
                    <img src={PublishingLabel} alt="Publishing" />
                    Publishing
                  </label>
                </div>
                <div>
                  <input
                    id="scienceLabel"
                    type="checkbox"
                    checked={isScience}
                    onChange={(e) => {
                      setIsScience(e.target.selected);
                    }}
                  />
                  <label for="scienceLabel">
                    <img src={ScienceLabel} alt="Science" />
                    Science
                  </label>
                </div>
              </div>
            </div>

            <div className={classes.newIdeaFeedback}>
              <p>
                Feedback <br /> Status
              </p>
              <div className={classes.feedbacks}>
                <div>
                  <p>Likes</p>

                  <label for="showLike" className={classes.filter}>
                    Show
                    <input
                      type="radio"
                      id="showLike"
                      name="Likes"
                      checked={showLikes}
                      onClick={() => {
                        setShowLikes(true);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>

                  <label for="hiddenLike" className={classes.filter}>
                    Hidden
                    <input
                      type="radio"
                      id="hiddenLike"
                      name="Likes"
                      checked={!showLikes}
                      onClick={() => {
                        setShowLikes(false);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>
                </div>
                <div>
                  <p>Views</p>

                  <label for="showView" className={classes.filter}>
                    Show
                    <input
                      type="radio"
                      id="showView"
                      name="Views"
                      checked={showViews}
                      onClick={() => {
                        setShowViews(true);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>

                  <label for="hiddenView" className={classes.filter}>
                    Hidden
                    <input
                      type="radio"
                      id="hiddenView"
                      name="Views"
                      checked={!showViews}
                      onClick={() => {
                        setShowViews(false);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>
                </div>
                <div>
                  <p>Comments</p>

                  <label for="showComments" className={classes.filter}>
                    Show
                    <input
                      type="radio"
                      id="showComments"
                      name="Comments"
                      checked={showComments}
                      onClick={() => {
                        setShowComments(true);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>

                  <label for="hiddenComments" className={classes.filter}>
                    Hidden
                    <input
                      type="radio"
                      id="hiddenComments"
                      name="Comments"
                      checked={!showComments}
                      onClick={() => {
                        setShowComments(false);
                      }}
                    />
                    <span className={classes.custom}></span>
                  </label>
                </div>
              </div>
            </div>

            <div className={classes.newIdeaOptions}>
              <button onClick={handleNext}>
                <img src={Next} alt="next" />
                Next
              </button>
            </div>
          </div>
        )}

        {activeStep === 1 && (
          <div className={classes.newIdeaDesc}>
            <div className={classes.ideaDesc}>
              <h3>Description</h3>
              <textarea
                value={ideaDescription}
                onChange={(e) => {
                  setIdeaDescription(e.target.value);
                }}
              />
            </div>

            <div className={classes.newIdeaOptions}>
              <button onClick={handleBack}>
                <img src={Previous} alt="previous" />
                Previous
              </button>
              <button onClick={setChangedData}>
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
          <div className={classes.uploadedFilesContainer}>
            <div className={classes.uploadedFiles}>
              <h3>Attach Files</h3>
              <div className={classes.manageUploadedFiles}>
                <div className={classes.attachFile}>
                  {isFileUploaded ? (
                    <button>
                      <img src={AttachFile} alt="attach_files" />
                      <label for="AttachFile">Attach</label>
                      <input
                        type="file"
                        id="AttachFile"
                        onChange={uploadAttachFile}
                      />
                    </button>
                  ) : (
                    <CircularProgress />
                  )}
                </div>

                {attachedFilesNum !== 0 && (
                  <div className={classes.uploadedFilesList}>
                    {attachedFiles.map((item, index) => (
                      <UploadedFile
                        key={index}
                        token={token}
                        uuid={item.uuid}
                        type={item.name.split(".")[1]}
                        fileName={item.name}
                        downloadOrDelete="delete"
                      />
                    ))}
                  </div>
                )}
              </div>
            </div>

            <div className={classes.uploadedFilesOptions}>
              <button onClick={handleBack}>
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

export default CreateIdea;
