import { React } from "react";
import classes from "./IdeaStructure.module.scss";
import Edit_Idea from "../../images/edit_idea.png";
import Collaboration_Request from "../../images/collaboration_request.png";
import Financial_Step from "../../images/evolution_step.png";
import { useLocation, Link, useParams } from "react-router-dom";
import {
  CollaborationRequest,
  FinancialStep,
  EditIdea,
} from "../../components";

const IdeaStructure = ({ token }) => {
  const location = useLocation();
  const url = location.pathname.split("/")[2];
  const params = useParams();
  const uuid = params.ideaId;

  return (
    <div className={classes.container}>
      <div className={classes.sidebar}>
        <Link
          className={classes.sidebarOptions}
          to={`/ideaStructure/editIdea/${uuid}`}
        >
          <img src={Edit_Idea} alt="Edit_Idea" /> Edit Idea
        </Link>
        <Link
          className={classes.sidebarOptions}
          to={`/ideaStructure/collaborationRequest/${uuid}`}
        >
          <img src={Collaboration_Request} alt="Collaboration_Request" />
          Collaboration Request
        </Link>
        <Link
          className={classes.sidebarOptions}
          to={`/ideaStructure/financialStep/${uuid}`}
        >
          <img src={Financial_Step} alt="Financial_Step" /> Financial Step
        </Link>
      </div>
      <div className={classes.main}>
        {
          {
            editIdea: <EditIdea uuid={uuid} token={token} />,
            collaborationRequest: (
              <CollaborationRequest uuid={uuid} token={token} />
            ),
            financialStep: <FinancialStep uuid={uuid} token={token} />,
          }[url]
        }
      </div>
    </div>
  );
};

export default IdeaStructure;
