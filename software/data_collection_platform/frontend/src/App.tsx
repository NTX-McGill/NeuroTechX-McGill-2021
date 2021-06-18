import React from "react";
import DataCollectionPage from "./DataCollectionPage";
import { youtubeLinks } from "./utils/links";
import "./App.scss";

const App = () => (
  <div className="App">
    <DataCollectionPage links={youtubeLinks} />
  </div>
);

export default App;
