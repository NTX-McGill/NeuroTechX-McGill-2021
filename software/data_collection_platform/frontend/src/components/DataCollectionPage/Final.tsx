import React from "react";
import { finalBackground } from "../../assets";

const Final = () => (
  <div className="Final">
    <div>
      <h1>Thank you!</h1>
      <p>
        NeuroTech is gathering data for a biofeedback product to help manage
        stress and anxiety levels using your own heart rate data. Thanks for
        helping us collect heart rate signals!
      </p>
      <p>
        If you have any questions about this process or our project, please
        contact the NeuroTech team at mcgillneurotech@gmail.com.
      </p>
    </div>
    <img alt="" src={finalBackground} />
  </div>
);

export default Final;
