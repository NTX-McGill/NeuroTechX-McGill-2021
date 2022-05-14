import React, { Component } from 'react';
import './Key.css';

export interface KeyProps {
  dispChar: string | JSX.Element;
  outputChar: string;
  phase: number;
  freq: number;
  color: string;
  width: string;
  isSelected: boolean;
}

class Key extends Component<KeyProps> {
  ref: any;

  constructor(props: KeyProps) {
    super(props);
    this.ref = React.createRef();
  }

  shouldComponentUpdate(nextProps: KeyProps) {
    if (
      nextProps.color === this.props.color &&
      nextProps.isSelected === this.props.isSelected
    ) {
      return false;
    }

    return true;
  }

  setColor(color: string) {
    this.ref.current.style.backgroundColor = color;
  }

  makeKeyStyle() {
    let keyStyle = {
      borderWidth: 0,
      width: this.props.width,
      backgroundColor: this.props.color,
    };

    if (this.props.isSelected) {
      keyStyle.borderWidth = 1;
    }

    return keyStyle;
  }

  render() {
    return (
      <button ref={this.ref} className="key-button" style={this.makeKeyStyle()}>
        {this.props.freq}
        <br />
        {this.props.dispChar}
      </button>
    );
  }
}

export default Key;
