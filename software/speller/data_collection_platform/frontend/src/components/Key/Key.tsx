import React, { Component } from "react"
import KeyProps from "./KeyProps";
import './Key.css';

class Key extends Component<KeyProps> {

  shouldComponentUpdate(nextProps: KeyProps){
    if (nextProps.color === this.props.color) {
      return false
    }

    return true
  }

     render() {

      return (            
        <button className="key-button" style={{backgroundColor: this.props.color, width: this.props.width}}>{this.props.freq}<br/>{this.props.dispChar}</button>
      );
     }
    }

export default Key;
