import classes from "./App.module.scss";
import { ForgotPassword, CreateAccount, Login, MainContainer } from "./pages";
import { Routes, Route } from "react-router-dom";

function App() {
  return (
    <div className={classes.container}>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/mainPage" element={<MainContainer />} />
        <Route path="/accountReport/:userId" element={<MainContainer />} />
        <Route path="/ideaReport/:ideaId" element={<MainContainer />} />
        <Route path="/forgotPassword" element={<ForgotPassword />} />
        <Route path="/showProfile/:userId" element={<MainContainer />} />
        <Route path="/profileStructure/profile" element={<MainContainer />} />
        <Route path="/profileStructure/myIdeas" element={<MainContainer />} />
        <Route
          path="/profileStructure/savedIdeas"
          element={<MainContainer />}
        />
        <Route
          path="/profileStructure/followings"
          element={<MainContainer />}
        />
        <Route path="/profileStructure/followers" element={<MainContainer />} />
        <Route
          path="/profileStructure/editProfile"
          element={<MainContainer />}
        />
        <Route
          path="/profileStructure/createIdea"
          element={<MainContainer />}
        />
        <Route path="/createAccount" element={<CreateAccount />} />
        <Route path="/login" element={<Login />} />
        <Route
          path="/stepsStructure/ideaShow/:ideaId"
          element={<MainContainer />}
        />
        <Route
          path="/stepsStructure/financialStepShow/:ideaId"
          element={<MainContainer />}
        />
        <Route
          path="/stepsStructure/collaborationRequestShow/:ideaId"
          element={<MainContainer />}
        />
        <Route
          path="/ideaStructure/collaborationRequest/:ideaId"
          element={<MainContainer />}
        />
        <Route
          path="/ideaStructure/financialStep/:ideaId"
          element={<MainContainer />}
        />
        <Route
          path="/ideaStructure/editIdea/:ideaId"
          element={<MainContainer />}
        />
      </Routes>
    </div>
  );
}

export default App;
