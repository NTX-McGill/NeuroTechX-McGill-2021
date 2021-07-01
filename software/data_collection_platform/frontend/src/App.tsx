import React from "react";
import DataCollectionPage from "./components/DataCollectionPage";
import { youtubeLinks } from "./utils/links";
import "./App.scss";

const App = () => (
  <div className="App">
    <DataCollectionPage videos={youtubeLinks} />
  </div>
);

export default App;
