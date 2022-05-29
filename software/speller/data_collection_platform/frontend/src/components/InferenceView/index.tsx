import * as React from 'react';
import './index.css';

const InferenceView = ({
  label,
  predictions,
  nextWord,
  setSentence
}: {
  label: string;
  predictions: { value: string; confidence: number }[];
  nextWord?: boolean;
  setSentence: Function;
}) => {
  const textLog = React.createRef<HTMLTextAreaElement>();

  const clearSentence = () => {
    setSentence("");
  }

  const parsedPredictions = React.useMemo(() => {
    return predictions.sort((a, b) => {
      if (a.confidence > b.confidence) return -1;
      else return 1;
    });
  }, [predictions]);

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
        <h5>{nextWord ? 'Next Word:' : 'Next Character:'}</h5>
        <div className={'predictions'}>
          {parsedPredictions.map((p, index) => (
            <h6 key={index}>{p.value}</h6>
          ))}
        </div>
        <button className="clear" onClick={clearSentence}>Clear</button>
      </div>
    </div>
  );
};

export default InferenceView;
