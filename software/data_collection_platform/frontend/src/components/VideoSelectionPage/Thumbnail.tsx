import React from "react";
import { VideoInfo } from "../../types";
import Checkbox from "@material-ui/core/Checkbox";

const Thumbnail = ({
  video,
  checked,
  onCheckChange,
}: {
  video: VideoInfo;
  checked: boolean;
  onCheckChange: (video: VideoInfo, checked: boolean) => void;
}) => {
  const onChange = () => {
    onCheckChange(video, !checked);
  };

  return (
    <div className="Thumbnail">
      <Checkbox {...{ checked, onChange }} />
      <img alt="" src={`http://img.youtube.com/vi/${video.youtube_id}/0.jpg`} />

      <div className="Info">
        <p>Stressful: {video.is_stressful ? "yes" : "no"}</p>
        <p>Keywords: {video.keywords.join(", ")}</p>
      </div>
    </div>
  );
};

export default Thumbnail;
