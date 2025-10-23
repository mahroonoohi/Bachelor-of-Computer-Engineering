import React from "react";
import classes from "./SavedIdeas.module.scss";
import IdeaFilter from "../../images/filter.png";
import { IdeaFilterSmallMenu } from "../SmallMenus";
import { useState, useEffect } from "react";
import axios from "axios";
import { useDispatch, useSelector } from "react-redux";
import { ideasActions } from "../../store/idea";
import { Idea, Skeleton } from "..";

const SavedIdeas = ({ token }) => {
  const dispatch = useDispatch();
  const userIdeas = useSelector((state) => state.ideas.ideas);
  const userIdeasNum = useSelector((state) => state.ideas.ideasNum);

  const [isShowMenu, setIsShowMenu] = useState(false);
  const [isLoading, setIsLoading] = useState(true);

  const [isArts, setIsArts] = useState(false);
  const [isGames, setIsGames] = useState(false);
  const [isDesignTech, setIsDesignTech] = useState(false);
  const [isFoodCraft, setIsFoodCraft] = useState(false);
  const [isFilms, setIsFilms] = useState(false);
  const [isMusics, setIsMusics] = useState(false);
  const [isPublishing, setIsPublishing] = useState(false);
  const [isScience, setIsScience] = useState(false);

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}idea/save-idea/`,
          {
            headers: {
              Authorization: "Bearer " + token,
            },
          }
        );
        console.log(res);
        dispatch(ideasActions.deleteAllIdeas());
        const ideas = res.data;
        for (const item of ideas) {
          dispatch(
            ideasActions.addIdea({
              uuid: item.idea.uuid,
              image: item.idea.image,
              title: item.idea.title,
              goal: item.idea.goal,
              details: item.idea.abstract,
              likes: item.idea.likes_count,
              views: item.idea.views_count,
              comments: item.idea.comments_count,
            })
          );
        }
        console.log(userIdeas);
        setIsLoading(false);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const applyFilter = async () => {
    const filter = [];
    isFilms && filter.push("films");
    isScience && filter.push("science");
    isPublishing && filter.push("publishing");
    isMusics && filter.push("music");
    isGames && filter.push("games");
    isFoodCraft && filter.push("food-craft");
    isDesignTech && filter.push("tech");
    isArts && filter.push("art");
    console.log(isArts);
    console.log(filter);

    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/filter/saved/`,
        {
          classification: filter,
        },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log(res);
      const ideas = res.data;
      dispatch(ideasActions.deleteAllIdeas());
      for (const item of ideas) {
        dispatch(
          ideasActions.addIdea({
            uuid: item.uuid,
            image: item.image,
            title: item.title,
            goal: item.goal,
            details: item.abstract,
            likes: item.likes_count,
            views: item.views_count,
            comments: item.comments_count,
          })
        );
      }
      console.log(userIdeas);
    } catch (err) {
      console.log(err);
    }
  };

  const showMenuHandler = () => {
    setIsShowMenu(!isShowMenu);
  };

  return (
    <div className={classes.body}>
      <div className={classes.titleContainer}>
        <h2>Saved Ideas</h2>
        <div className={classes.smallIdeaFilterMenu}>
          <button
            className={classes.smallIdeaFilterMenuBTN}
            onClick={showMenuHandler}
          >
            <img src={IdeaFilter} alt="IdeaFilter" />
          </button>
          <IdeaFilterSmallMenu
            isShowMenu={isShowMenu}
            setIsArts={setIsArts}
            setIsGames={setIsGames}
            setIsDesignTech={setIsDesignTech}
            setIsFoodCraft={setIsFoodCraft}
            setIsFilms={setIsFilms}
            setIsMusics={setIsMusics}
            setIsPublishing={setIsPublishing}
            setIsScience={setIsScience}
            applyFilter={applyFilter}
          />
        </div>
      </div>
      <div className={classes.main}>
        <div className={classes.ideasContainer}>
          {userIdeasNum !== 0 && (
            <div className={classes.ideas}>
              {isLoading ? (
                <Skeleton type="Idea" />
              ) : (
                userIdeas.map((item, index) => (
                  <Idea
                    key={index}
                    type="SavedIdeas"
                    uuid={item.uuid}
                    token={token}
                    title={item.title}
                    image={item.image}
                    goal={item.goal}
                    details={item.details}
                    likes={item.likes}
                    views={item.views}
                    comments={item.comments}
                  />
                ))
              )}
            </div>
          )}
        </div>
        <div className={classes.ideaFilter}>
          <h3>Filters</h3>

          <label for="Arts" className={classes.filter}>
            Arts
            <input
              type="checkbox"
              value="1"
              id="Arts"
              onChange={(e) => {
                setIsArts(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="DesignTech" className={classes.filter}>
            Tech
            <input
              type="checkbox"
              value="1"
              id="DesignTech"
              onChange={(e) => {
                setIsDesignTech(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="FoodCraft" className={classes.filter}>
            Food & Craft
            <input
              type="checkbox"
              value="1"
              id="FoodCraft"
              onChange={(e) => {
                setIsFoodCraft(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="Games" className={classes.filter}>
            Games
            <input
              type="checkbox"
              value="1"
              id="Games"
              onChange={(e) => {
                setIsGames(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="Films" className={classes.filter}>
            Films
            <input
              type="checkbox"
              value="1"
              id="Films"
              onChange={(e) => {
                setIsFilms(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="Music" className={classes.filter}>
            Music
            <input
              type="checkbox"
              value="1"
              id="Music"
              onChange={(e) => {
                setIsMusics(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="Publishing" className={classes.filter}>
            Publishing
            <input
              type="checkbox"
              value="1"
              id="Publishing"
              onChange={(e) => {
                setIsPublishing(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <label for="Science" className={classes.filter}>
            Science
            <input
              type="checkbox"
              value="1"
              id="Science"
              onChange={(e) => {
                setIsScience(e.target.checked);
              }}
            />
            <span className={classes.custom}></span>
          </label>

          <button className={classes.applyFilter} onClick={applyFilter}>
            Apply Filter
          </button>
        </div>
      </div>
    </div>
  );
};

export default SavedIdeas;
