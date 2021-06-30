import React, { useState } from "react";
import { IconButton } from "@material-ui/core";
import { ArrowBack, ArrowForward } from "@material-ui/icons";
import { logo } from "../assets";
import api from "../api";
import "./index.scss";

import Welcome from "./Welcome";
import Video from "./Video";
import Feedback, { FeedbackValue } from "./Feedback";
import Final from "./Final";

const DataCollectionPage = ({ links }: { links: string[] }) => {
  // Highest possible integer value for status.
  const endIndex = 2 * links.length;

  // status === -1 corresponds to the Welcome page.
  // status === endIndex corresponds to the Final page.
  //
  // Otherwise, we are either on a video or feedback page.
  // Status 2n corresponds to nth video, and 2n+1 corresponds
  // to nth feedback page.
  const [status, setStatus] = useState<number>(-1);

  const isWelcome = status === -1;
  const isFinal = status === endIndex;
  const isFeedback = !isWelcome && !isFinal && status % 2 !== 0;
  const index = Math.floor(status / 2);

  const [feedback, setFeedback] = useState<FeedbackValue | null>(null);

  const onClickPrev = () => setStatus(Math.max(-1, status - 1));
  const onClickNext = () => {
    if (isFeedback && feedback !== null) {
      api.sendFeedback({ url: links[index], stress_level: feedback });
    }
    setStatus(Math.min(endIndex, status + 1));
  };

  const Main = isWelcome ? (
    <Welcome
      timeEstimate={`${links.length * 2} minutes`}
      videoCount={`${links.length}`}
    />
  ) : isFinal ? (
    <Final />
  ) : status % 2 === 0 ? (
    <Video {...{ index, links }} />
  ) : (
    <Feedback {...{ index, links }} value={feedback} onChange={setFeedback} />
  );

  return (
    <div className="DataCollectionPage">
      <header>
        <img id="header-logo" src={logo} alt="Logo" />
        <div>McGill NeuroTech</div>
      </header>
      <main>{Main}</main>
      <nav>
        <IconButton className="arrow-prev" onClick={onClickPrev}>
          <ArrowBack />
        </IconButton>
        <IconButton className="arrow-next" onClick={onClickNext}>
          <ArrowForward />
        </IconButton>
      </nav>
    </div>
  );
};
export default DataCollectionPage;
