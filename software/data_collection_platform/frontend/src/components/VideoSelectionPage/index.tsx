import React, { useEffect } from "react";
import { useSelector, useDispatch } from "../../hooks";
import { videos as videosActions } from "../../state";
import { VideoInfo } from "../../types";
import Thumbnail from "./Thumbnail";
import "./index.scss";

const VideoSelectionPage = () => {
  const dispatch = useDispatch();
  const { videos, videosToWatch } = useSelector((state) => state.videos);

  const checked = videosToWatch.reduce(
    (acc, v) => acc.add(v.id),
    new Set<number>()
  );

  useEffect(() => {
    if (!videos.length) dispatch(videosActions.fetch());
  }, [dispatch, videos.length]);

  const handleOnCheckChange = (video: VideoInfo, checked: boolean) => {
    const newVideosToWatch = checked
      ? [...videosToWatch, { ...video }]
      : videosToWatch.filter((vid) => vid.id !== video.id);

    dispatch(videosActions.setVideosToWatch(newVideosToWatch));
  };

  return (
    <div className="VideoSelectionPage">
      <h1>Select At Least 1 Video To Watch</h1>
      <div className="VideoSelectionContainer">
        {videos.map((video) => (
          <Thumbnail
            key={video.id}
            video={video}
            checked={checked.has(video.id)}
            onCheckChange={handleOnCheckChange}
          />
        ))}
      </div>
    </div>
  );
};

export default VideoSelectionPage;
