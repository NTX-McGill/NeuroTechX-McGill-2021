import React, { Component } from 'react';
import './Key.css';

export interface KeyProps {
  dispChar: string | JSX.Element;
  outputChar: string;
  phase: number;
  freq: number;
  color: string;
  width: string;
}

class Key extends Component<KeyProps> {

  ref: any

  constructor(props: KeyProps){
    super(props)
    this.ref = React.createRef()
  }

  shouldComponentUpdate(nextProps: KeyProps){
    if (nextProps.color === this.props.color) {
      return false
    }

    return true
  }

  setColor(color: string){
    this.ref.current.style.backgroundColor = color
  }

  render() {
    return (            
      <button ref={this.ref} className="key-button" style={{backgroundColor: this.props.color, width: this.props.width}}>{this.props.freq}<br/>{this.props.dispChar}</button>
    );
  }
}

export default Key;

