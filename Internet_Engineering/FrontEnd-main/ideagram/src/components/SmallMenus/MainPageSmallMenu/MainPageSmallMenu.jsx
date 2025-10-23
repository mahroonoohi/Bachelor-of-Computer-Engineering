import React from "react";
import classes from "./MainPageSmallMenu.module.scss";

const MainPageSmallMenu = ({ showMenuHandler, isShowMenu, applyFilter }) => {
  return (
    <ul
      className={`${classes.menu} ${
        isShowMenu ? classes.visible : classes.invisible
      }`}
    >
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("art");
          }}
        >
          Arts
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("tech");
          }}
        >
          Tech
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("food-craft");
          }}
        >
          Food
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("games");
          }}
        >
          Games
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("films");
          }}
        >
          Films
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("music");
          }}
        >
          Music
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("publishing");
          }}
        >
          Publishing
        </button>
      </li>
      <li onClick={showMenuHandler}>
        <button
          onClick={() => {
            applyFilter("science");
          }}
        >
          Science
        </button>
      </li>
    </ul>
  );
};

export default MainPageSmallMenu;
