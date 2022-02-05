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

const COLOR_DEFAULT = '#000000';
const COLOR_HIGHLIGHT_START = '#ff0000';
const COLOR_HIGHLIGHT_STOP = '#0000ff';

const WIDTH_DEFAULT = '3.3rem';

const COLOR_RUN = '#2ede28';
const COLOR_STOP = '#ff0000';

const DURATION_HIGHLIGHT = 1000;
const DURATION_FLASHING = 15000;
const DURATION_REST = 1000;

interface KeyMap {
  [key: string]: KeyProps;
}

interface KeyboardState {
  keys: KeyMap;
  running: boolean;
  unFlashedKeys: string[];
  numRoundsCollected: number;
}

interface KeyboardProps {
  chartData: any[];
  setChartData: Dispatch<SetStateAction<any[]>>;
}

class Keyboard extends Component<KeyboardProps, KeyboardState> {
  keyFlashing: string;
  keys: KeyMap;

  startTime: number;
  prevTime: number;

  callback: Function;

  plot: any[];

  processID: number;
  listRefs: any;

  constructor(props: KeyboardProps) {
    super(props);
    this.keys = {} as KeyMap;
    this.state = {
      running: false,
      keys: {} as KeyMap,
      numRoundsCollected: 0,
      unFlashedKeys: [] as string[],
    };
    this.keyFlashing = '';
    this.startTime = -1;
    this.prevTime = -1;
    this.callback = () => {};
    this.plot = props.chartData;
    this.processID = -1;
    for (let val in Object.keys(config)) {
      let temp = { ...this.listRefs };
      temp[Object.keys(config)[val]] = React.createRef();
      this.listRefs = temp;
    }
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

    if (delta < DURATION_FLASHING) {
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
    if (!this.state.running) {
      return;
    }

    if (this.processID === -1) {
      try {
        this.processID = (await startBCI()).data.pid;
        console.log(this.processID);
      } catch (error) {
        console.error(error);
      }
    }

    // don't collect from same key twice
    const numKeys = this.state.unFlashedKeys.length;
    const randIdx = Math.floor(Math.random() * numKeys);
    const randKey = this.state.unFlashedKeys[randIdx];

    const newState = { ...this.state.keys };
    newState[randKey].color = COLOR_HIGHLIGHT_START;

    const unFlashedKeys = this.state.unFlashedKeys;
    unFlashedKeys.splice(randIdx, 1);

    this.setState({ keys: newState, unFlashedKeys });

    this.keyFlashing = randKey;

    console.info('Collecting data for:', randKey);

    setTimeout(async () => {
      try {
        await startCollectingKey(
          this.processID,
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
        for (let val in this.listRefs) {
          this.listRefs[val].current.setColor(COLOR_DEFAULT);
        }

        try {
          await stopCollectingKey(this.processID);
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
              this.startCollection();
            }
          }, DURATION_REST);
        }, DURATION_HIGHLIGHT);
      };

      this.startFlash();
    }, DURATION_HIGHLIGHT);
  }

  async start() {
    if (this.processID !== -1) {
      try {
        await stopBCI(this.processID);
      } catch (error) {
        console.error(error);
      }
    }

    if (!this.state.running) {
      this.setState(
        {
          running: true,
          unFlashedKeys: Object.keys(this.keys),
          numRoundsCollected: this.state.numRoundsCollected + 1,
        },
        () => this.startCollection()
      );
    } else {
      this.setState({ running: false });
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

  render() {
    return (
      <div className={'keyboard'}>
        {this.listOfRows().map(rowNum => (
          <div key={rowNum} className="keys-div">
            {this.keysByRow(rowNum).map(key => this.getKey(key as string))}
          </div>
        ))}

        <button
          className="toggle"
          style={{ background: this.getToggleColor() }}
          onClick={this.start.bind(this)}
        >
          {this.state.running
            ? 'Stop'
            : this.state.numRoundsCollected > 0
            ? 'Collect Again'
            : 'Start'}
        </button>
      </div>
    );
  }
}

export default Keyboard;
