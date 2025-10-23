import { React, useState, useEffect } from "react";
import classes from "./Followers.module.scss";
import { UserAccount } from "..";
import axios from "axios";

const Followers = ({ token }) => {
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

        const followerRes = await axios.get(
          `${process.env.REACT_APP_API_ADDRESS}user/profile/followers/${res.data.username}`
        );
        console.log(followerRes);
        setUserFollowers(followerRes.data);
      } catch (err) {
        console.log(err);
      }
    };
    getUserData();
  }, []);

  return (
    <div className={classes.body}>
      <h2>Followers</h2>

      <div className={classes.followers}>
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

export default Followers;
