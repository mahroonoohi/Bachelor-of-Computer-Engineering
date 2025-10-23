import React from "react";
import classes from "./UploadedFile.module.scss";
import pdfFile from "../../images/pdfFile.png";
import jpgFile from "../../images/jpgFile.png";
import pptxFile from "../../images/pptxFile.png";
import docFile from "../../images/docFile.png";
import DeleteFile from "../../images/delete.png";
import downloadFile from "../../images/downloadIcon.png";
import axios from "axios";
import { useDispatch } from "react-redux";
import { attachedFilesActions } from "../../store/attachedFilesForIdea";
import { Link } from "react-router-dom";

const UploadedFile = ({ uuid, token, type, fileName, downloadOrDelete }) => {
  const dispatch = useDispatch();

  const deleteFile = async () => {
    try {
      const res = await axios.delete(
        `${process.env.REACT_APP_API_ADDRESS}idea/attachment/detail/${uuid}`,

        {
          headers: {
            Authorization: "Bearer " + token,
          },
        }
      );
      console.log(res);
      dispatch(
        attachedFilesActions.deleteAttachedFiles({
          uuid: uuid,
        })
      );
    } catch (e) {
      console.log(e);
    }
  };

  return (
    <div className={classes.container}>
      <div className={classes.deleteDownloadFile}>
        {downloadOrDelete === "download" && (
          <a
            href={`http://api.iwantnet.space:8001${fileName}`}
            target="_blank"
            rel="noreferrer"
            download
          >
            <button className={classes.download}>
              <img src={downloadFile} alt="download_file" />
              Download
            </button>
          </a>
        )}
        {downloadOrDelete === "delete" && (
          <button className={classes.delete} onClick={deleteFile}>
            <img src={DeleteFile} alt="delete_file" />
            Delete
          </button>
        )}
      </div>
      <div className={classes.uploadedFile}>
        {
          {
            pdf: <img src={pdfFile} alt="pdfFile" />,
            jpg: <img src={jpgFile} alt="jpgFile" />,
            gif: <img src={jpgFile} alt="jpgFile" />,
            jpeg: <img src={jpgFile} alt="jpgFile" />,
            png: <img src={jpgFile} alt="jpgFile" />,
            svg: <img src={jpgFile} alt="jpgFile" />,
            pptx: <img src={pptxFile} alt="pptxFile" />,
            doc: <img src={docFile} alt="docFile" />,
          }[type]
        }
        <h3>{fileName}</h3>
      </div>
    </div>
  );
};

export default UploadedFile;
