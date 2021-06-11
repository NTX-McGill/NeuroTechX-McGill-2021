import React, { useState } from "react";
import { IconButton } from "@material-ui/core";
import { ArrowBack, ArrowForward } from "@material-ui/icons";
import { logo } from "./assets";
import "./DataCollectionPage.scss";

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
  const index = Math.floor(status / 2);

  const onClickPrev = () => setStatus(Math.max(-1, status - 1));
  const onClickNext = () => setStatus(Math.min(endIndex, status + 1));

  const Main = isWelcome ? (
    <Welcome
      timeEstimate={`${links.length * 2} minutes`}
      videoCount={`${links.length}`}
    />
  ) : isFinal ? (
    <Final />
  ) : status % 2 === 0 ? (
    <Video url={links[index]} />
  ) : (
    <Feedback url={links[index]} />
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

const Video = ({ url }: { url: string }) => {
  return <div>Video for {url}</div>;
};

const Feedback = ({ url }: { url: string }) => {
  return <div>Feedback for {url}</div>;
};
