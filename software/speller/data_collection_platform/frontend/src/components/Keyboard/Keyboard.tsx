import React, { Component } from 'react';
import Key from '../Key/Key';

import config from '../../keyboard_config.json';
import KeyboardState from './KeyboardState';
import KeyProps from '../Key/KeyProps';
import KeyMap from './KeyMap';

import KeyboardBackspaceIcon from '@material-ui/icons/KeyboardBackspace';
import SpaceBarIcon from '@material-ui/icons/SpaceBar';

import {
  LineChart,
  Line,
  XAxis,
  Tooltip,
  CartesianGrid,
  YAxis,
} from 'recharts';

import './Keyboard.css';

class Keyboard extends Component<{}, KeyboardState> {
  COLOR_DEFAULT = '#000000';
  COLOR_HIGHLIGHT_START = '#ff0000';
  COLOR_HIGHLIGHT_STOP = '#0000ff';

  WIDTH_DEFAULT = '50px';
  WIDTH_SPACE = '330px';

  COLOR_RUN = '#2ede28';
  COLOR_STOP = '#ff0000';

  DURATION_HIGHLIGHT = 1000;
  DURATION_FLASHING = 15000;
  DURATION_REST = 1000;

  keyFlashing: string;

  keys: KeyMap;

  startTime: number;
  prevTime: number;

  callback: Function;

  plot: any[];

  constructor(props: any) {
    super(props);
    this.keys = {} as KeyMap;
    this.state = { keys: {} as KeyMap, running: false, plot: [] };
    this.keyFlashing = '';
    this.startTime = -1;
    this.prevTime = -1;
    this.callback = () => {};
    this.plot = [];
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

    const newState = { ...this.state.keys };

    var delta = time - this.startTime;

    for (let key in newState) {
      const info = newState[key];

      var sine_value =
        0.5 *
        (1 + Math.sin(2 * Math.PI * info.freq * (delta / 1000) + info.phase));

      newState[key].color = this.hexToRGBA(
        this.COLOR_DEFAULT,
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

      if (delta < this.DURATION_FLASHING) {
        this.prevTime = time;
        window.requestAnimationFrame(this.flash);
      } else {
        this.setState({ plot: this.plot });
        this.callback();
      }
    });
  };

  startFlash() {
    this.startTime = -1;
    //plot
    this.setState({ plot: [] });
    this.plot = [];
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
    newState[randKey].color = this.COLOR_HIGHLIGHT_START;

    this.setState({ keys: newState });

    this.keyFlashing = randKey;

    console.log('Collecting data for:', randKey);

    setTimeout(() => {
      newState[randKey].color = this.COLOR_DEFAULT;
      this.setState({ keys: newState });

      //opacity flashing

      this.callback = () => {
        newState[randKey].color = this.COLOR_HIGHLIGHT_STOP;
        this.setState({ keys: newState });

        setTimeout(() => {
          newState[randKey].color = this.COLOR_DEFAULT;
          this.setState({ keys: newState });

          setTimeout(() => {
            if (this.state.running) {
              this.startCollection();
            }
          }, this.DURATION_REST);
        }, this.DURATION_HIGHLIGHT);
      };

      this.startFlash();
    }, this.DURATION_HIGHLIGHT);
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
      color: this.COLOR_DEFAULT,
      width: this.WIDTH_DEFAULT,
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
    return !this.state.running ? this.COLOR_RUN : this.COLOR_STOP;
  }

  render() {
    return (
      <div>
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

        <LineChart
          width={1400}
          height={400}
          data={this.state.plot}
          margin={{ top: 5, right: 20, left: 10, bottom: 5 }}
        >
          <XAxis
            type="number"
            dataKey="name"
            domain={[0, 15]}
            tickCount={16}
            allowDataOverflow={true}
          />
          <YAxis type="number" domain={[0, 1]} yAxisId={0} />
          <YAxis type="number" yAxisId={1} />
          <YAxis type="number" yAxisId={2} />
          <Tooltip />
          <CartesianGrid stroke="#f5f5f5" />
          <Line type="monotone" dataKey="value" stroke="#ff7300" yAxisId={0} />
          <Line type="monotone" dataKey="diff" stroke="#088F8F" yAxisId={1} />
          <Line type="monotone" dataKey="int" stroke="#E6E6FA" yAxisId={2} />
        </LineChart>
      </div>
    );
  }
}

export default Keyboard;
