import React, { useEffect } from "react";
import { useSelector, useDispatch } from "../../hooks";
import { videos as videosActions } from "../../state";
import { VideoInfo } from "../../types";
import Thumbnail from "./Thumbnail";
import {
  VideoSelectionContainer,
  SelectionPageContainer,
} from "./__styled__/VideoSelectionPage";

const VideoSelectionPage = () => {
  const dispatch = useDispatch();
  const { videos, videosToWatch } = useSelector((state) => state.videos);

  useEffect(() => {
    if (!videos.length) dispatch(videosActions.fetch());
  }, [dispatch, videos.length]);

  const handleOnCheckChange = (video: VideoInfo, checked: boolean) => {
    // add video to the list of videos in the state if checked else remove the video from the list
    const newVideosToWatch = checked
      ? [...videosToWatch, { ...video }]
      : videosToWatch.filter((vid) => vid.id !== video.id);

    dispatch(videosActions.setVideosToWatch(newVideosToWatch));
  };

  return (
    <SelectionPageContainer>
      <h1>Select At Least 1 Video To Watch</h1>
      <VideoSelectionContainer>
        {videos.map((video) => (
          <Thumbnail
            key={video.id}
            video={video}
            onCheckChange={handleOnCheckChange}
          />
        ))}
      </VideoSelectionContainer>
    </SelectionPageContainer>
  );
};

export default VideoSelectionPage;
