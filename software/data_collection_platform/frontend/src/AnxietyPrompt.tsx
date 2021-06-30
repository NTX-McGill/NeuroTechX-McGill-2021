import React, { useState, useEffect } from "react";
import api from "./api";
import "./AnxietyPrompt.scss";

const AnxietyPrompt = () => {
  const [anxious, setAnxious] = useState<boolean>(false);

  useEffect(() => {
    const keydown = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        api.anxiousStart({ time: new Date().toISOString() });
        setAnxious(true);
      }
    };
    const keyup = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        api.anxiousStop({ time: new Date().toISOString() });
        setAnxious(false);
      }
    };
    document.addEventListener("keydown", keydown);
    document.addEventListener("keyup", keyup);
    return () => {
      document.removeEventListener("keydown", keydown);
      document.removeEventListener("keyup", keyup);
    };
  }, []);

  return (
    <div className="AnxietyPrompt">
      Hold space if you're feeling anxious
      <br />
      {anxious ? "Anxious" : "Calm"}
    </div>
  );
};
export default AnxietyPrompt;
