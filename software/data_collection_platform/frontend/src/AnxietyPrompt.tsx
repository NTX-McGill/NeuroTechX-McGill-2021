import React, { useState, useEffect, useRef } from "react";
import { anxiousPeriods } from "./state";
import { useDispatch } from "./hooks";
import "./AnxietyPrompt.scss";

const AnxietyPrompt = () => {
  const [anxious, setAnxious] = useState<boolean>(false);
  const startTime = useRef<string | null>(null);
  const dispatch = useDispatch();

  useEffect(() => {
    const keydown = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        startTime.current = new Date().toISOString();
        setAnxious(true);
      }
    };
    const keyup = (e: KeyboardEvent) => {
      if (e.code === "Space") {
        if (startTime.current !== null) {
          const period: [string, string] = [
            startTime.current,
            new Date().toISOString(),
          ];
          dispatch(anxiousPeriods.addPeriod(period));
        }
        setAnxious(false);
      }
    };
    document.addEventListener("keydown", keydown);
    document.addEventListener("keyup", keyup);
    return () => {
      document.removeEventListener("keydown", keydown);
      document.removeEventListener("keyup", keyup);
    };
  }, [dispatch]);

  return (
    <div className="AnxietyPrompt">
      Hold space if you're feeling anxious
      <br />
      {anxious ? "Anxious" : "Calm"}
    </div>
  );
};
export default AnxietyPrompt;
