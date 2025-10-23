import React from "react";
import classes from "./UserMediaLinkElement.module.scss";
import Delete from "../../../images/delete2.png";
import { useDispatch } from "react-redux";
import { userMediaLinksActions } from "../../../store/userMediaLink";
import axios from "axios";

const UserMediaLinkElement = ({ uuid, amount, title, details, token }) => {
  const dispatch = useDispatch();

  const deleteMediaLinkHandler = async () => {
    await axios.delete(
      `${process.env.REACT_APP_API_ADDRESS}user/social-media/${uuid}`,

      {
        headers: {
          Authorization: "Bearer " + token,
        },
      }
    );

    dispatch(
      userMediaLinksActions.deleteUserMediaLink({
        title: title,
      })
    );
  };

  return (
    <div className={classes.container}>
      <p>{amount}</p>
      <h4>{title}</h4>
      <button onClick={deleteMediaLinkHandler}>
        <img src={Delete} alt="Delete" />
      </button>
    </div>
  );
};

export default UserMediaLinkElement;
