import React, { useState, useEffect } from "react";
import { IconButton } from "@material-ui/core";
import { ArrowBack, ArrowForward } from "@material-ui/icons";
import { logo } from "../../assets";
import api from "../../api";
import "./index.scss";
import { VideoInfo, FeedbackValue } from "../../types";

import Welcome from "./Welcome";
import Video from "./Video";
import Feedback from "./Feedback";
import Final from "./Final";

const DataCollectionPage = ({ videos }: { videos: VideoInfo[] }) => {
  // Highest possible integer value for status.
  const endIndex = 2 * videos.length;

  // status === -1 corresponds to the Welcome page.
  // status === endIndex corresponds to the Final page.
  //
  // Otherwise, we are either on a video or feedback page.
  // Status 2n corresponds to nth video, and 2n+1 corresponds
  // to nth feedback page.
  const [status, setStatus] = useState<number>(-1);

  const [feedback, setFeedback] = useState<FeedbackValue | null>(null);
  const [videoEnded, setVideoEnded] = useState<boolean>(false);

  const isWelcome = status === -1;
  const isFinal = status === endIndex;
  const isFeedback = !isWelcome && !isFinal && status % 2 !== 0;
  const isVideo = !isWelcome && !isFinal && status % 2 === 0;
  const index = Math.floor(status / 2);

  const nextDisabled =
    (isFeedback && feedback == null) || (isVideo && !videoEnded);

  console.log(isVideo);
  console.log(nextDisabled);

  const onClickPrev = () => {
    setStatus(Math.max(-1, status - 1));
    setVideoEnded(false);
  };
  const onClickNext = () => {
    if (isFeedback && feedback !== null) {
      api.sendFeedback({ url: videos[index].url, stress_level: feedback });
      setFeedback(null);
    }
    setStatus(Math.min(endIndex, status + 1));
    setVideoEnded(false);
  };

  const onStart = () => {
    api.videoStart();
  };

  const onEnded = () => {
    api.videoStop();
    setVideoEnded(true);
  };

  useEffect(() => {
    const keydown = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        api.anxiousStart();
      }
    };
    const keyup = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        api.anxiousStop();
      }
    };
    document.addEventListener("keydown", keydown);
    document.addEventListener("keyup", keyup);
    return () => {
      document.removeEventListener("keydown", keydown);
      document.removeEventListener("keyup", keyup);
    };
  }, []);

  const Main = isWelcome ? (
    <Welcome
      timeEstimate={`${videos.length * 2} minutes`}
      videoCount={`${videos.length}`}
    />
  ) : isFinal ? (
    <Final />
  ) : status % 2 === 0 ? (
    <Video {...{ index, videos, onStart, onEnded }} />
  ) : (
    <Feedback {...{ index, videos }} value={feedback} onChange={setFeedback} />
  );

  return (
    <div className="DataCollectionPage">
      <header>
        <img id="header-logo" src={logo} alt="Logo" />
        <div>McGill NeuroTech</div>
      </header>
      <main>{Main}</main>
      {!isFinal && (
        <nav>
          <IconButton className="arrow-prev" onClick={onClickPrev}>
            <ArrowBack />
          </IconButton>
          <IconButton
            className="arrow-next"
            onClick={onClickNext}
            disabled={nextDisabled}
          >
            <ArrowForward />
          </IconButton>
        </nav>
      )}
    </div>
  );
};
export default DataCollectionPage;
