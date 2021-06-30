import React from "react";

const Video = ({ index, links }: { index: number; links: string[] }) => {
  return (
    <div>
      <h1>
        Viewing video {index + 1} of {links.length}
      </h1>
    </div>
  );
};
export default Video;
