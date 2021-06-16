import React, { useState } from "react";
import { IconButton, Radio } from "@material-ui/core";
import { ArrowBack, ArrowForward } from "@material-ui/icons";
import { logo } from "./assets";
import api from "./api";
import "./DataCollectionPage.scss";

type FeedbackValue = 1 | 2 | 3;

const DataCollectionPage = ({ links }: { links: string[] }) => {
  // Highest possible integer value for status.
  const endIndex = 2 * links.length;

  // status === -1 corresponds to the Welcome page.
  // status === endIndex corresponds to the Final page.
  //
  // Otherwise, we are either on a video or feedback page.
  // Status 2n corresponds to nth video, and 2n+1 corresponds
  // to nth feedback page.
  const [status, setStatus] = useState<number>(-1);

  const isWelcome = status === -1;
  const isFinal = status === endIndex;
  const isFeedback = !isWelcome && !isFinal && status % 2 !== 0;
  const index = Math.floor(status / 2);

  const [feedback, setFeedback] = useState<FeedbackValue | null>(null);

  const onClickPrev = () => setStatus(Math.max(-1, status - 1));
  const onClickNext = () => {
    if (isFeedback && feedback !== null) {
      api.sendFeedback({ url: links[index], stress_level: feedback });
    }
    setStatus(Math.min(endIndex, status + 1));
  };

  const Main = isWelcome ? (
    <Welcome
      timeEstimate={`${links.length * 2} minutes`}
      videoCount={`${links.length}`}
    />
  ) : isFinal ? (
    <Final />
  ) : status % 2 === 0 ? (
    <Video {...{ index, links }} />
  ) : (
    <Feedback {...{ index, links }} value={feedback} onChange={setFeedback} />
  );

  return (
    <div className="DataCollectionPage">
      <header>
        <img id="header-logo" src={logo} alt="Logo" />
        <div>McGill NeuroTech</div>
      </header>
      <main>{Main}</main>
      <nav>
        <IconButton className="arrow-prev" onClick={onClickPrev}>
          <ArrowBack />
        </IconButton>
        <IconButton className="arrow-next" onClick={onClickNext}>
          <ArrowForward />
        </IconButton>
      </nav>
    </div>
  );
};
export default DataCollectionPage;

const Welcome = ({
  timeEstimate,
  videoCount,
}: {
  timeEstimate: string;
  videoCount: string;
}) => (
  <div>
    <h1>Welcome!</h1>
    <p>
      NeuroTech is gathering data for a biofeedback product to help manage
      stress and anxiety levels using your own heart rate data. Thanks for
      helping us collect heart rate signals!
    </p>
    <p>
      This process will take around {timeEstimate}. You will be asked to watch{" "}
      {videoCount} videos that might either make you calm or stressed.
    </p>
    <p>
      These videos may induce anxiety in some individuals. If watching a certain
      video makes you uncomfortable, you are always able to skip it.
    </p>

    <h1>Task Instructions</h1>
    <p>
      We need to measure your heart rate signals as you watch the video on the
      next page.
    </p>
    <p>
      To identify when you are stressed, please <b>press and hold the button</b>{" "}
      when you feel any stress. For example, if a spider enters the screen and
      spiders cause you stress, you would press down the button when it enters
      and release the button when it leaves. If nothing happens that causes you
      stress, you do not have to press down the button at all.
    </p>
    <p>
      If you make a mistake pressing the button during the video, you can{" "}
      <b>restart</b> the video. You can also <b>skip</b> this video if it makes
      you uncomfortable.
      <br />
    </p>
    <p>
      <i>
        <b>After the video</b> you will be asked if you experienced stress
        during the video and if so, to rate your stress level from 1 to 5.
      </i>
    </p>
  </div>
);

const Final = () => <div>End!</div>;

const Video = ({ index, links }: { index: number; links: string[] }) => {
  return (
    <div>
      <h1>
        Viewing video {index + 1} of {links.length}
      </h1>
    </div>
  );
};

const Feedback = ({
  index,
  links,
  value,
  onChange,
}: {
  index: number;
  links: string[];
  value: FeedbackValue | null;
  onChange?: (v: FeedbackValue) => void;
}) => {
  const isFinal = index + 1 === links.length;

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
            Before we start video {index + 2} of {links.length}, please take a
            minute to relax yourself. Whenever you feel ready, please continue
            to the next page. As a reminder, you are allowed to skip the video
            at any point if it makes you uncomfortable.
          </p>
        </>
      )}
    </div>
  );
};
