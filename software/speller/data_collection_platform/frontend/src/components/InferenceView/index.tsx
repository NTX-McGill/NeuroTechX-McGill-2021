import * as React from 'react';
import './index.css';

const InferenceView = ({
  label,
  predictions,
  setSentence
}: {
  label: string;
  predictions: string[];
  setSentence: Function;
}) => {
  const textLog = React.createRef<HTMLTextAreaElement>();

  const clearSentence = () => {
    setSentence("");
  }

  React.useEffect(() => {
    if (textLog.current) {
      textLog.current.scrollTop = textLog.current.scrollHeight;
      //textLog.current.style.height = textLog.current.scrollHeight + 'px';
    }
  }, [textLog]);

  return (
    <div className={'main-container'}>
      <textarea ref={textLog} value={label} readOnly={true}/>
      <div className={'p-container'}>
        <h5>{"Autocomplete:"}</h5>
        <div className={'predictions'}>
          {predictions.map((p, index) => (
            <h6 key={index}>{p}</h6>
          ))}
        </div>
        <button className="clear" onClick={clearSentence}>Clear</button>
      </div>
    </div>
  );
};

export default InferenceView;
