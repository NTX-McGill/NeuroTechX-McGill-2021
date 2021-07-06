import React, { useState, useEffect } from "react";
import { useSelector } from "../../hooks";
import { IconButton } from "@material-ui/core";
import { ArrowBack, ArrowForward } from "@material-ui/icons";
import { logo } from "../../assets";
import api from "../../api";
import "./index.scss";
import { FeedbackValue } from "../../types";
import VideoSelectionPage from "../VideoSelectionPage";
import Welcome from "./Welcome";
import Video from "./Video";
import Feedback from "./Feedback";
import Final from "./Final";

const DataCollectionPage = () => {
  const videos = useSelector((st) => st.videos.videosToWatch);

  // Highest possible integer value for status.
  const endIndex = 2 * videos.length;

  // status === -1 corresponds to the Welcome page.
  // status === endIndex corresponds to the Final page.
  //
  // Otherwise, we are either on a video or feedback page.
  // Status 2n corresponds to nth video, and 2n+1 corresponds
  // to nth feedback page.
  const [status, setStatus] = useState<number>(-2);

  const [feedback, setFeedback] = useState<FeedbackValue | null>(null);
  const [videoEnded, setVideoEnded] = useState<boolean>(false);

  const clearState = () => {
    setFeedback(null);
    setVideoEnded(false);
  };

  const isWelcome = status === -2;
  const isSelection = status === -1;
  const isFinal = status === endIndex;
  const isFeedback = 0 <= status && !isFinal && status % 2 !== 0;
  const isVideo = 0 <= status && !isFinal && status % 2 === 0;
  const index = Math.floor(status / 2);

  const nextDisabled =
    (isSelection && videos.length === 0) ||
    (isFeedback && feedback == null) ||
    (isVideo && !videoEnded);

  const onClickPrev = () => {
    setStatus(Math.max(-2, status - 1));
    clearState();
  };
  const onClickNext = () => {
    if (isFeedback && feedback !== null) {
      api.sendFeedback({
        video_id: videos[index].id,
        stress_level: feedback,
      });
      setFeedback(null);
    }
    setStatus(Math.min(endIndex, status + 1));
    clearState();
  };

  const onStart = () => {
    api.videoStart();
  };

  const onEnded = () => {
    api.videoStop();
    setVideoEnded(true);
  };

  useEffect(() => {
    api.openBciStart();
  }, []);

  useEffect(() => {
    if (isFinal) api.openBciStop();
  }, [isFinal]);

  useEffect(() => {
    const keydown = (e: KeyboardEvent) => {
      if (e.code === "Space" && !e.repeat) {
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
  ) : isSelection ? (
    <VideoSelectionPage />
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
