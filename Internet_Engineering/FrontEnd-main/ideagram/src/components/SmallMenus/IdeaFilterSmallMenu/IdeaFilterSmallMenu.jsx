import React from "react";
import classes from "./IdeaFilterSmallMenu.module.scss";

const IdeaFilterSmallMenu = ({
  isShowMenu,
  setIsArts,
  setIsGames,
  setIsDesignTech,
  setIsFoodCraft,
  setIsFilms,
  setIsMusics,
  setIsPublishing,
  setIsScience,
  applyFilter,
}) => {
  return (
    <div
      className={`${classes.ideaFilter} ${
        isShowMenu ? classes.visible : classes.invisible
      }`}
    >
      <h3>Filters</h3>

      <label for="ArtsSmallMenu" className={classes.filter}>
        Arts
        <input
          type="checkbox"
          value="1"
          id="ArtsSmallMenu"
          onChange={(e) => {
            setIsArts(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="DesignTechSmallMenu" className={classes.filter}>
        Tech
        <input
          type="checkbox"
          value="1"
          id="DesignTechSmallMenu"
          onChange={(e) => {
            setIsDesignTech(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="FoodCraftSmallMenu" className={classes.filter}>
        Food & Craft
        <input
          type="checkbox"
          value="1"
          id="FoodCraftSmallMenu"
          onChange={(e) => {
            setIsFoodCraft(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="GamesSmallMenu" className={classes.filter}>
        Games
        <input
          type="checkbox"
          value="1"
          id="GamesSmallMenu"
          onChange={(e) => {
            setIsGames(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="FilmsSmallMenu" className={classes.filter}>
        Films
        <input
          type="checkbox"
          value="1"
          id="FilmsSmallMenu"
          onChange={(e) => {
            setIsFilms(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="MusicSmallMenu" className={classes.filter}>
        Music
        <input
          type="checkbox"
          value="1"
          id="MusicSmallMenu"
          onChange={(e) => {
            setIsMusics(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="PublishingSmallMenu" className={classes.filter}>
        Publishing
        <input
          type="checkbox"
          value="1"
          id="PublishingSmallMenu"
          onChange={(e) => {
            setIsPublishing(e.target.checked);
          }}
        />
        <span className={classes.custom}></span>
      </label>

      <label for="ScienceSmallMenu" className={classes.filter}>
        Science
        <input
          type="checkbox"
          value="1"
          id="ScienceSmallMenu"
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
  );
};

export default IdeaFilterSmallMenu;
