import React from "react";
import { Radio } from "@material-ui/core";
import { FeedbackValue, VideoInfo } from "../../types";

const Feedback = ({
  index,
  videos,
  value,
  onChange,
}: Readonly<{
  index: number;
  videos: VideoInfo[];
  value: FeedbackValue | null;
  onChange?: (v: FeedbackValue) => void;
}>) => {
  const isFinal = index + 1 === videos.length;

  const onChange_ = ({ target: { value } }) =>
    onChange?.(parseInt(value) as FeedbackValue);

  return (
    <div>
      <h1>Feedback</h1>
      <h2>How would you rate your overall stress level from that video?</h2>
      <div className="feedback-form">
        <label>
          Not stressed at all
          <Radio value={"1"} checked={value === 1} onChange={onChange_} />
        </label>
        <Radio value={"2"} checked={value === 2} onChange={onChange_} />
        <label>
          <Radio value={"3"} checked={value === 3} onChange={onChange_} />
          Extremely stressed
        </label>
      </div>

      {!isFinal && (
        <>
          <h2>Take some breaths to relax yourself before the next video</h2>
          <p>
            Before we start video {index + 2} of {videos.length}, please take a
            minute to relax yourself. Whenever you feel ready, please continue
            to the next page. As a reminder, you are allowed to skip the video
            at any point if it makes you uncomfortable.
          </p>
        </>
      )}
    </div>
  );
};
export default Feedback;
