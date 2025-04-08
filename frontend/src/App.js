import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";

import AuthPage from "./page/AuthPage";
import HomePage from "./page/HomePage";

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/home" element={<HomePage />} />
        <Route path="/" element={<AuthPage />} />
      </Routes>
    </Router>
  );
}

export default App;
