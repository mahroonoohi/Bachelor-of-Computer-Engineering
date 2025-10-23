import { React, useEffect } from "react";
import classes from "./MainPage.module.scss";
import { Idea, Skeleton } from "../../components";
import { useState } from "react";
import Menu from "../../images/burger-menu.png";
import { MainPageSmallMenu } from "../../components/SmallMenus";
import axios from "axios";

const MainPage = ({ token }) => {
  const [seeAll, setSeeAll] = useState(false);
  const [isLoading, setIsLoading] = useState(true);
  const [userIdeas, setUserIdeas] = useState([]);

  const [isShowMenu, setIsShowMenu] = useState(false);
  const [isShowOptionsMenu, setIsShowOptionsMenu] = useState(false);

  const showMenuHandler = () => {
    setIsShowOptionsMenu(false);
    setIsShowMenu(!isShowMenu);
  };

  useEffect(() => {
    const getUserData = async () => {
      try {
        const res = await axios.post(
          `${process.env.REACT_APP_API_ADDRESS}idea/filter/`
        );
        console.log(res);
        const list = res.data;
        list.sort((a, b) =>
          a.views_count !== null &&
          b.views_count !== null &&
          a.views_count > b.views_count
            ? 1
            : a.views_count !== null &&
              b.views_count !== null &&
              b.views_count > a.views_count
            ? -1
            : 0
        );
        setUserIdeas(list);
        setIsLoading(false);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  const applyFilter = async (filterItem) => {
    try {
      const res = await axios.post(
        `${process.env.REACT_APP_API_ADDRESS}idea/filter/`,
        {
          classification: [filterItem],
        },
        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log(res.data);
      setUserIdeas(res.data);
    } catch (err) {
      console.log(err);
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.toolbar}>
        <button
          onClick={() => {
            applyFilter("art");
          }}
        >
          Arts
        </button>
        <button
          onClick={() => {
            applyFilter("tech");
          }}
        >
          Tech
        </button>
        <button
          onClick={() => {
            applyFilter("food-craft");
          }}
        >
          Food
        </button>
        <button
          onClick={() => {
            applyFilter("games");
          }}
        >
          Games
        </button>
        <button
          onClick={() => {
            applyFilter("films");
          }}
        >
          Films
        </button>
        <button
          onClick={() => {
            applyFilter("music");
          }}
        >
          Music
        </button>
        <button
          onClick={() => {
            applyFilter("publishing");
          }}
        >
          Publishing
        </button>
        <button
          onClick={() => {
            applyFilter("science");
          }}
        >
          Science
        </button>
      </div>

      <div className={classes.body}>
        <div className={classes.seeAllContainer}>
          <h1>Ideas</h1>

          <div className={classes.optionsContainer}>
            <button
              className={`${classes.seeAllIdeas} ${
                seeAll && classes.disableButton
              }`}
              onClick={() => setSeeAll(true)}
              disabled={seeAll}
            >
              See All
            </button>
            <div className={classes.smallMenu}>
              <button className={classes.showMenuBTN} onClick={showMenuHandler}>
                <img src={Menu} alt="menu" />
              </button>

              <MainPageSmallMenu
                showMenuHandler={showMenuHandler}
                isShowMenu={isShowMenu}
                applyFilter={applyFilter}
              />
            </div>
          </div>
        </div>

        <div className={classes.ideasContainer}>
          <div className={`${classes.ideas} ${seeAll && classes.scrollable}`}>
            {isLoading ? (
              <Skeleton type="Idea" />
            ) : (
              <>
                {seeAll
                  ? userIdeas.map((item, index) => (
                      <Idea
                        type="MainPage"
                        key={index}
                        uuid={item.uuid}
                        token={token}
                        title={item.title}
                        image={item.image}
                        goal={item.goal}
                        details={item.details}
                        likes={item.likes_count}
                        views={item.views_count}
                        comments={item.comments_count}
                        isShowLikes={item.likes_count === null ? false : true}
                        isComments={item.comments_count === null ? false : true}
                        isShowViews={item.views_count === null ? false : true}
                      />
                    ))
                  : userIdeas.map(
                      (item, index) =>
                        index < 6 && (
                          <Idea
                            type="MainPage"
                            key={index}
                            uuid={item.uuid}
                            token={token}
                            title={item.title}
                            image={item.image}
                            goal={item.goal}
                            details={item.details}
                            likes={item.likes_count}
                            views={item.views_count}
                            comments={item.comments_count}
                            isShowLikes={
                              item.likes_count === null ? false : true
                            }
                            isComments={
                              item.comments_count === null ? false : true
                            }
                            isShowViews={
                              item.views_count === null ? false : true
                            }
                          />
                        )
                    )}
              </>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default MainPage;
