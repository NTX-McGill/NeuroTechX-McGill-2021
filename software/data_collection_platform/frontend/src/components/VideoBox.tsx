import React, { useState } from "react";
import { IconButton } from "@material-ui/core";
import NavigateNextIcon from "@material-ui/icons/NavigateNext";
import { youtubeLinks } from "../utils/links";

const VideoBox = () => {
  const [currVideoIndex, setCurrVideoIndex] = useState<number>(0);

  const handleOnClickNext = () => {
    setCurrVideoIndex((currVideoIndex + 1) % youtubeLinks.length);
  };

  return (
    <>
      <iframe
        width="1120"
        height="630"
        src={youtubeLinks[currVideoIndex].url}
        title="YouTube video player"
        frameBorder="0"
        allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
        allowFullScreen
      />
      <IconButton onClick={handleOnClickNext}>
        <NavigateNextIcon />
      </IconButton>
    </>
  );
};

export default VideoBox;
