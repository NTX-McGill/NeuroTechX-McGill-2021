import KeyMap from './KeyMap';

interface KeyboardState {
  keys: KeyMap;
  running: boolean;
  [key: string]: any;
}

export default KeyboardState;
