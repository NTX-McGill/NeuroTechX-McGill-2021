import React, { Component, Dispatch, SetStateAction } from 'react';
import './Keyboard.css';

import config from '../../keyboard_config.json';

import Key, { KeyProps } from '../Key/Key';
import SpaceBarIcon from '@material-ui/icons/SpaceBar';
import KeyboardBackspaceIcon from '@material-ui/icons/KeyboardBackspace';

import {
  startBCI,
  stopBCI,
  startCollectingKey,
  stopCollectingKey,
} from '../../api';
import { ThreeSixty } from '@material-ui/icons';

var current_duration_flashing : number;
var current_duration_rest : number;

const COLOR_DEFAULT = '#000000';
const COLOR_HIGHLIGHT_START = '#ff0000';

const COLOR_HIGHLIGHT_STOP = '#000000';

const WIDTH_DEFAULT = '7rem';

const COLOR_RUN = '#2ede28';
const COLOR_PAUSE = '#F2C94C';
const COLOR_STOP = '#ff0000';

const DURATION_HIGHLIGHT_START = 1000;
const DURATION_HIGHLIGHT_STOP = 100;
const DURATION_FLASHING = 5000;
const DURATION_REST = 1000;

const DURATION_FLASHING_INFERENCE = 1000;
const DURATION_REST_INFERENCE = 1000;

interface KeyMap {
  [key: string]: KeyProps;
}

interface KeyboardState {
  keys: KeyMap;
  running: boolean;
  resting: boolean;
  unFlashedKeys: string[];
  numRoundsCollected: number;
  collectorName: string;
}

interface KeyboardProps {
  chartData: any[];
  setChartData: Dispatch<SetStateAction<any[]>>;
  useInference: boolean;
  setSentence: Function;
}

class Keyboard extends Component<KeyboardProps, KeyboardState> {
  keyFlashing: string;
  keys: KeyMap;

  startTime: number;
  prevTime: number;

  callback: Function;

  plot: any[];

  processID: number;
  inferenceProcessID: number;
  listRefs: any;

  sentence: string;

  constructor(props: KeyboardProps) {
    super(props);
    this.keys = {} as KeyMap;
    this.state = {
      running: false,
      resting: false,
      keys: {} as KeyMap,
      numRoundsCollected: 0,
      unFlashedKeys: [] as string[],
      collectorName: '',
    };
    this.keyFlashing = '';
    this.startTime = -1;
    this.prevTime = -1;
    this.callback = () => {};
    this.plot = props.chartData;
    this.processID = -1;
    this.inferenceProcessID = -1;

    this.sentence = "";

    for (let val in Object.keys(config)) {
      let temp = { ...this.listRefs };
      temp[Object.keys(config)[val]] = React.createRef();
      this.listRefs = temp;
    }

    this.onNameChange = this.onNameChange.bind(this);
  }

  hexToRGBA(hex: string, alpha: string) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + alpha + ')';
  }

  flash = (time: number) => {
    var a = performance.now();

    if (this.startTime === -1) {
      this.startTime = time;
      this.prevTime = time;
    }

    var b = performance.now();

    const newState = { ...this.state.keys };

    var c = performance.now();

    var delta = time - this.startTime;

    for (let key in newState) {
      const info = newState[key];

      var sine_value =
        0.5 *
        (1 + Math.sin(2 * Math.PI * info.freq * (delta / 1000) + info.phase));

      //newState[key].color = this.hexToRGBA(this.COLOR_DEFAULT, sine_value.toString())

      this.listRefs[key].current.setColor(
        this.hexToRGBA(COLOR_DEFAULT, sine_value.toString())
      );
    }

    if (this.prevTime === this.startTime) {
      this.plot.push({ name: delta / 1000 });
    } else {
      this.plot.push({
        name: delta / 1000,
        diff: 1000 / (time - this.prevTime),
      });
    }

    if (delta < current_duration_flashing) {
      this.prevTime = time;
      window.requestAnimationFrame(this.flash);
    } else {
      //this.setState({plot: this.plot})
      //this.props.setChartData([...this.plot]);
      this.callback();
    }
  };

  startFlash() {
    this.startTime = -1;
    this.plot = [];
    this.props.setChartData([]);
    window.requestAnimationFrame(this.flash);
  }

  async startCollection() {
    if (!this.state.running) return;
    if (this.processID === -1) {
      try {
        this.processID = (
          await startBCI(this.state.collectorName)
        ).data.data.pid;

        console.log(this.processID);
      } catch (error) {
        console.error(error);
        // TODO: Make a popup showing a message that the BCI stream has not started 
        return;
      }
    }

    // don't collect from same key twiceß
    const numKeys = this.state.unFlashedKeys.length;
    const randIdx = Math.floor(Math.random() * numKeys);
    const randKey = this.state.unFlashedKeys[randIdx];

    const newState = { ...this.state.keys };
    newState[randKey].color = COLOR_HIGHLIGHT_START;

    const unFlashedKeys = this.state.unFlashedKeys;
    if (unFlashedKeys.length === 0) {
      try {
        await stopBCI(this.processID);
        this.setState({ running: false });
        return;
      } catch (error) {
        console.error(error);
      }
    }
    unFlashedKeys.splice(randIdx, 1);

    this.setState({ keys: newState, unFlashedKeys });

    this.keyFlashing = randKey;

    console.info('Collecting data for:', randKey);

    setTimeout(async () => {
      try {
        await startCollectingKey(
          this.processID,
          false,
          randKey,
          config[randKey as keyof typeof config].phase,
          config[randKey as keyof typeof config].frequency
        );
      } catch (error) {
        console.error(error);
      }
      newState[randKey].color = COLOR_DEFAULT;
      this.setState({ keys: newState });

      // opacity flashing

      this.callback = async () => {
        this.setState({ resting: true });
        for (let val in this.listRefs) {
          this.listRefs[val].current.setColor(COLOR_DEFAULT);
        }

        try {
          await stopCollectingKey(this.processID, false);
        } catch (error) {
          console.error(error);
        }

        for (let val in this.listRefs) {
          this.listRefs[val].current.setColor(COLOR_DEFAULT);
        }

        newState[randKey].color = COLOR_HIGHLIGHT_STOP;
        this.setState({ keys: newState });

        setTimeout(() => {
          newState[randKey].color = COLOR_DEFAULT;
          this.setState({ keys: newState });

          setTimeout(async () => {
            if (this.state.running) {
              this.setState({ resting: false });
              this.startCollection();
            }
          }, DURATION_REST);
        }, DURATION_HIGHLIGHT_STOP);
      };

      this.startFlash();
    }, DURATION_HIGHLIGHT_START);
  }

  async startInferenceHelper() {
    try {
      await startCollectingKey(
        this.inferenceProcessID,
        true
      );
    } catch (error) {
      console.error(error);
    }

    this.setState({ resting: false, running: true});
    this.startFlash.bind(this)();
  }

  async startInference() {

    console.log("Collector:", this.state.collectorName);

    this.inferenceProcessID = (
      await startBCI()
    ).data.data.pid;

    console.log("Inference process:", this.inferenceProcessID);

    current_duration_flashing = DURATION_FLASHING_INFERENCE;
    current_duration_rest = DURATION_REST_INFERENCE;

    this.callback = async () => {

      this.setState({ resting: true });

      for (let val in this.listRefs) {
        this.listRefs[val].current.setColor(COLOR_DEFAULT);
      }

      try {
        this.sentence = (await stopCollectingKey(this.inferenceProcessID, true, this.sentence)).data.sentence;
        this.props.setSentence(this.sentence);
        console.log(this.sentence);
      } catch (error) {
        console.error(error);
      }

      setTimeout(async () => {

        if (this.state.running) {

          this.startInferenceHelper();

        }
      }, DURATION_REST_INFERENCE);

      //this.setState({ keys: newState });
    }

    this.startInferenceHelper();

    //setInterval(this.startFlash.bind(this), DURATION_REST_INFERENCE);
  }

  start() {

    if (this.props.useInference === true) {
      this.startInference();
      return;
    }

    current_duration_flashing = DURATION_FLASHING;
    current_duration_rest = DURATION_REST;

    if (this.state.running) return;
    return this.setState(
      {
        running: true,
        resting: false,
        unFlashedKeys: Object.keys(this.keys),
        numRoundsCollected: this.state.numRoundsCollected + 1,
      },
      () => this.startCollection()
    );
  }

  async stopInference() {

    this.sentence = "";

    try {
      this.sentence = (await stopCollectingKey(this.inferenceProcessID, true, this.sentence)).data.sentence;
      this.props.setSentence(this.sentence);

      await stopBCI(this.inferenceProcessID);
      this.inferenceProcessID = -1;
    } catch (error) {
      console.error(error);
    }

    this.setState({
      running: false,
      resting: false,
    });
  }

  async stop() {

    if (!this.state.resting) return;

    if (this.props.useInference === true) {
      this.stopInference();
      return;
    }

    if (this.processID !== -1) {
      try {
        await stopBCI(this.processID);

        // reset process id when stopping collection for current round.
        this.processID = -1;
      } catch (error) {
        console.error(error);
      }
    }

    this.keyFlashing = '';
    this.setState({
      running: false,
      resting: false,
    });
  }

  pauseInference() {
    console.log(this.state.running);

    if (this.state.running) {
      
      this.setState({ running: false })
    } else {
      this.setState({ running: true }, () => {
        this.startInferenceHelper();
      });
    }
  }

  pause() {

    if (this.props.useInference === true) {
      this.pauseInference();
      return;
    }

    if (this.state.running) {
      this.setState({ running: false });
    } else {
      this.setState({ running: true, resting: false }, () => {
        return this.startCollection();
      });
    }
  }

  listOfRows() {
    return [
      ...new Set(
        Object.keys(config).map(item => config[item as keyof typeof config].row)
      ),
    ].sort();
  }

  keysByRow(rowNum: number): String[] {
    return Object.keys(config)
      .filter(key => config[key as keyof typeof config].row === rowNum)
      .sort((a, b) => {
        if (
          config[a as keyof typeof config].order >
          config[b as keyof typeof config].order
        ) {
          return 1;
        } else if (
          config[a as keyof typeof config].order <
          config[b as keyof typeof config].order
        ) {
          return -1;
        }

        return 0;
      });
  }

  getKey(key: string) {
    var keyInfo = {
      dispChar: key.toUpperCase(),
      outputChar: key,
      freq: config[key as keyof typeof config].frequency,
      phase: config[key as keyof typeof config].phase,
      color: COLOR_DEFAULT,
      width: WIDTH_DEFAULT,
    } as KeyProps;

    switch (key) {
      case '\\s': {
        keyInfo.dispChar = <SpaceBarIcon />;
        keyInfo.outputChar = ' ';
        break;
      }
      case '\b': {
        keyInfo.dispChar = <KeyboardBackspaceIcon />;
        break;
      }
      default: {
        break;
      }
    }

    this.keys[key as keyof typeof config] = keyInfo;

    return (
      <Key
        ref={this.listRefs[key]}
        key={key}
        dispChar={keyInfo.dispChar}
        outputChar={keyInfo.outputChar}
        freq={keyInfo.freq}
        phase={keyInfo.phase}
        isSelected={key === this.keyFlashing}
        color={this.state.keys[key as keyof typeof config]?.color}
        width={keyInfo.width}
      />
    );
  }

  componentDidMount() {
    this.setState({ keys: this.keys, running: false });
  }

  getToggleColor() {
    return !this.state.running ? COLOR_RUN : COLOR_STOP;
  }

  onNameChange(e: React.FormEvent<HTMLInputElement>) {
    this.setState({ collectorName: e.currentTarget.value });
  }

  render() {
    return (
      <div className={'keyboard'}>
        {this.listOfRows().map(rowNum => (
          <div key={rowNum} className="keys-div">
            {this.keysByRow(rowNum).map(key => this.getKey(key as string))}
          </div>
        ))}

        <div style={{ flexDirection: 'row' }}>
          {!this.state.running && !this.state.resting && (
            <button
              className="toggle"
              onClick={this.start.bind(this)}
              style={{ background: COLOR_RUN }}
            >
              {this.state.numRoundsCollected > 0 ? 'Collect Again' : 'Start'}
            </button>
          )}
          {this.state.resting && (
            <>
              <button
                className="toggle"
                style={{ background: COLOR_STOP }}
                onClick={this.stop.bind(this)}
              >
                Stop
              </button>
              <button
                className="toggle"
                disabled={!this.state.collectorName}
                style={{ backgroundColor: COLOR_PAUSE }}
                onClick={this.pause.bind(this)}
              >
                {this.state.running ? 'Pause' : 'Resume'}
              </button>
            </>
          )}
        </div>
        {!this.props.useInference ? 
        
        (<label>
          Collector name
          <br />
          <input
            value={this.state.collectorName}
            onChange={this.onNameChange}
          />
        </label>) :

          (
            <select>
              <option value="S02">S02</option>
              <option value="S08">S08</option>
            </select>
          )

        }
      </div>
    );
  }
}

export default Keyboard;
