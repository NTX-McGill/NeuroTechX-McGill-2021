import React, { memo } from 'react';
import './Key.css';

export interface KeyProps {
  dispChar: string | JSX.Element;
  outputChar: string;
  phase: number;
  freq: number;
  color: string;
  width: string;
}

const Key = ({ color, width, freq, dispChar }: KeyProps) => (
  <button className="key-button" style={{ backgroundColor: color, width }}>
    {freq}
    <br />
    {dispChar}
  </button>
);

export default memo(Key, (props: KeyProps, nextProps: KeyProps) => {
  // only re-render key if the colour prop changes
  return nextProps.color === props.color;
});
