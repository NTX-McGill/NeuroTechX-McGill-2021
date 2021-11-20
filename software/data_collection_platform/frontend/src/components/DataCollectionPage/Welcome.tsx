const Welcome = ({
  timeEstimate,
  videoCount,
  error,
}: Readonly<{
  timeEstimate: string;
  videoCount: string;
  error?: string;
}>) => (
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

    {error && <p className="error">{error}</p>}
  </div>
);
export default Welcome;
