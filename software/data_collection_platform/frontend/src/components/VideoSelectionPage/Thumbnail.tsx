import React, { useState } from "react";
import { useSelector } from "../../hooks";
import { VideoInfo } from "../../types";
import Checkbox from "@material-ui/core/Checkbox";
import {
  ThumbnailContainer,
  InfoContainer,
} from "./__styled__/VideoSelectionPage";

const Thumbnail = ({
  video,
  onCheckChange,
}: {
  video: VideoInfo;
  onCheckChange: (video: VideoInfo, checked: boolean) => void;
}) => {
  const videosToWatch = useSelector((state) => state.videos.videosToWatch);

  const [checked, setChecked] = useState(
    videosToWatch.filter((vid) => vid.id === video.id).length > 0,
  );

  const handleOnCheckChange = () => {
    onCheckChange(video, !checked);
    setChecked(!checked);
  };

  return (
    <ThumbnailContainer>
      <Checkbox checked={checked} onChange={handleOnCheckChange} />
      <img alt="" src={`http://img.youtube.com/vi/${video.youtube_id}/0.jpg`} />

      <InfoContainer>
        <p>Stressful: {`${video.is_stressful}`}</p>
        <p>
          Keywords:{" "}
          {video.keywords.map((kw, i) =>
            i !== video.keywords.length - 1 ? `${kw}, ` : kw,
          )}
        </p>
      </InfoContainer>
    </ThumbnailContainer>
  );
};

export default Thumbnail;
