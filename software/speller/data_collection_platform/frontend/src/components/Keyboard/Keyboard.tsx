import React, { Component, Dispatch, SetStateAction } from 'react';
import './Keyboard.css';

import config from '../../keyboard_config.json';

import Key, { KeyProps } from '../Key/Key';
import SpaceBarIcon from '@material-ui/icons/SpaceBar';

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
  [key: string]: any;
}

interface KeyboardProps {
  chartData: any[],
  setChartData: Dispatch<SetStateAction<any[]>>
}

class Keyboard extends Component<KeyboardProps, KeyboardState> {
  keyFlashing: string;
  keys: KeyMap;

  startTime: number;
  prevTime: number;

  callback: Function;

  plot: any[];

  constructor(props: KeyboardProps) {
    super(props);
    this.keys = {} as KeyMap;
    this.state = { keys: {} as KeyMap, running: false };
    this.keyFlashing = '';
    this.startTime = -1;
    this.prevTime = -1;
    this.callback = () => {};
    this.plot = props.chartData;
  }

  hexToRGBA(hex: string, alpha: string) {
    const r = parseInt(hex.slice(1, 3), 16);
    const g = parseInt(hex.slice(3, 5), 16);
    const b = parseInt(hex.slice(5, 7), 16);

    return 'rgba(' + r + ', ' + g + ', ' + b + ', ' + alpha + ')';
  }

  flash = (time: number) => {
    if (this.startTime === -1) {
      this.startTime = time;
      this.prevTime = time;
    }

    const newState = { ...this.state.keys };

    var delta = time - this.startTime;

    for (let key in newState) {
      const info = newState[key];

      var sine_value =
        0.5 *
        (1 + Math.sin(2 * Math.PI * info.freq * (delta / 1000) + info.phase));

      newState[key].color = this.hexToRGBA(
        COLOR_DEFAULT,
        sine_value.toString()
      );
    }

    this.setState({ keys: newState }, () => {
      //console.log(performance.now()-a)

      if (this.prevTime === this.startTime) {
        this.plot.push({ name: delta / 1000, value: sine_value });
      } else {
        this.plot.push({
          name: delta / 1000,
          value: sine_value,
          diff: 1000 / (time - this.prevTime),
        });
      }

      if (delta < DURATION_FLASHING) {
        this.prevTime = time;
        window.requestAnimationFrame(this.flash);
      } else {
        this.props.setChartData([...this.plot]);
        this.callback();
      }
    });
  };

  startFlash() {
    this.startTime = -1;
    this.plot = [];
    this.props.setChartData([]);
    window.requestAnimationFrame(this.flash);
  }

  startCollection() {
    if (!this.state.running) {
      return;
    }

    const numKeys = Object.keys(this.state.keys).length;
    const randIdx = Math.floor(Math.random() * numKeys);
    const randKey = Object.keys(this.state.keys)[randIdx];

    const newState = { ...this.state.keys };
    newState[randKey].color = COLOR_HIGHLIGHT_START;

    this.setState({ keys: newState });

    this.keyFlashing = randKey;

    console.info('Collecting data for:', randKey);

    setTimeout(() => {
      newState[randKey].color = COLOR_DEFAULT;
      this.setState({ keys: newState });

      //opacity flashing

      this.callback = () => {
        newState[randKey].color = COLOR_HIGHLIGHT_STOP;
        this.setState({ keys: newState });

        setTimeout(() => {
          newState[randKey].color = COLOR_DEFAULT;
          this.setState({ keys: newState });

          setTimeout(() => {
            if (this.state.running) {
              this.startCollection();
            }
          }, DURATION_REST);
        }, DURATION_HIGHLIGHT);
      };

      this.startFlash();
    }, DURATION_HIGHLIGHT);
  }

  start() {
    this.setState({ running: !this.state.running }, () => {
      this.startCollection();
    });
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
      default: {
        break;
      }
    }

    this.keys[key as keyof typeof config] = keyInfo;

    return (
      <Key
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
    this.setState({ keys: this.keys });
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
          {!this.state.running ? 'Start' : 'Stop'}
        </button>
      </div>
    );
  }
}

export default Keyboard;
