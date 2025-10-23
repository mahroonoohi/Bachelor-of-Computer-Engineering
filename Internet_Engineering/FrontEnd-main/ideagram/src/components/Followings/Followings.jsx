import { React, useState, useEffect } from "react";
import classes from "./Followings.module.scss";
import { UserAccount } from "..";
import axios from "axios";

const Followings = ({ token }) => {
  const [userUserName, setUserUserName] = useState("");
  const [userFollowers, setUserFollowers] = useState([]);

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
        const followingRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/followings/${res.data.username}`
        );
        console.log(followingRes);
        setUserFollowers(followingRes.data);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  return (
    <div className={classes.body}>
      <h2>Followings</h2>

      <div className={classes.followings}>
        {userFollowers.map((item) => (
          <UserAccount
            profileImage={item.profile_image}
            name={`${item.first_name} ${item.last_name}`}
            followers={item.follower_count}
            followings={item.following_count}
          />
        ))}
      </div>
    </div>
  );
};

export default Followings;
