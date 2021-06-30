import React from "react";
import ReactPlayer, { ReactPlayerProps } from "react-player";
import { VideoInfo } from "../../types";

interface Props
  extends Omit<ReactPlayerProps, "url" | "config" | "width" | "height"> {
  index: number;
  videos: VideoInfo[];
}

const Video = ({ index, videos, ...rest }: Readonly<Props>) => {
  const { url, start, end } = videos[index];

  return (
    <div>
      <h1>
        Viewing video {index + 1} of {videos.length}
      </h1>

      <ReactPlayer
        url={url}
        config={{
          youtube: {
            playerVars: {
              start,
              end,
            },
          },
        }}
        {...rest}
      />
    </div>
  );
};
export default Video;
