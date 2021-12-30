import React, { Component } from "react"
import KeyProps from "./KeyProps";
import './Key.css';

class Key extends Component<KeyProps> {
  
     render() {
      return (            
        <button className="key-button">{this.props.freq}<br/>{this.props.dispChar}</button>
      );
     }
    }

export default Key;
