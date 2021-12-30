import React, { Component } from "react"
import Key from "../Key/Key"

import config from "../../keyboard_config.json"

class Keyboard extends Component {

    listOfRows() {
        return [...new Set(Object.keys(config).map(item => config[item as keyof typeof config].row))].sort();
    }

    keysByRow(rowNum: number) : String[] {
        return Object.keys(config).filter(key => config[key as keyof typeof config].row === rowNum).sort((a, b) => {
            if (config[a as keyof typeof config].order > config[b as keyof typeof config].order) {
                return 1;
            }
            else if (config[a as keyof typeof config].order < config[b as keyof typeof config].order) {
                return -1;
            }

            return 0;
        })
    }

    getKey(key: string) {

        switch(key) { 
            case "\s": { 
               break; 
            } 
            default: { 
               break; 
            } 
         }

        return (
            <Key 
            dispChar={key.toUpperCase()}
            outputChar={key}
            freq={config[key as keyof typeof config].frequency}
            phase={config[key as keyof typeof config].phase}
            >
            </Key>
        ) 
    }

    render() {
      return (            
        <div>
            {this.listOfRows().map(rowNum =>
            <div className="keys-div">
                {this.keysByRow(rowNum).map(key => this.getKey(key as string))}
            </div>
            )}
        </div>
      );
     }
    }

export default Keyboard;
