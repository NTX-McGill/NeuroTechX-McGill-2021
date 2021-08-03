import ReactPlayer, { ReactPlayerProps } from "react-player";
import { VideoInfo } from "../../types";

interface Props
  extends Omit<ReactPlayerProps, "url" | "config" | "width" | "height"> {
  index: number;
  videos: VideoInfo[];
}

const Video = ({ index, videos, ...rest }: Readonly<Props>) => {
  const { youtube_url, start, end } = videos[index];

  return (
    <div>
      <h1>
        Viewing video {index + 1} of {videos.length}
      </h1>

      <ReactPlayer
        className="ReactPlayer"
        url={youtube_url}
        config={{
          youtube: {
            playerVars: {
              start,
              end,
              autoplay: 1,
              disablekb: 1,
            },
          },
        }}
        {...rest}
      />
    </div>
  );
};
export default Video;
