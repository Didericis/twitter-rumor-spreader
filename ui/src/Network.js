import React from 'react';
import { Graph } from 'react-d3-graph';
import * as d3 from 'd3';

import './Network.css';
import api from './api';
import Instructions from './Instructions';

function CustomViewComponent({ isSelected, isRumor, isOrigin, retweetProb }) {
  let borderRadius = '0';
  let border = 'none';
  let background = '#222';
  if (isSelected) {
      border = '1px solid orange';
  }
  const scale = d3.scalePow()
    .exponent(.1)
    .domain([-1000, 1000])
    .range([0, 1])

  if (retweetProb) {
    background = d3.interpolateRdBu(scale(retweetProb.factor_scale))
  }
  if (isRumor) {
    background = "#053061";
    borderRadius = '1rem';
  }
  if (isOrigin) {
    background = 'orange';
    borderRadius = '1rem';
  }

  return (
    <div style={{ background, border, boxSizing: 'border-box', borderRadius, width: '1rem', height: '1rem', color: 'black' }} />
  )
}

export default class Network extends React.Component {
  state = {
    isDeterministic: true,
    isViewingInstructions: true,
    selected: 'fubuloubu',
    tweet: '',
    retweeted: [],
    network: {},
    retweetProbs: {},
    data: {
      nodes: [
        { id: 'fubuloubu' },
      ],
      links: []
    }
  }
  constructor(props) {
    super(props);
    this.graph = React.createRef();
  }
  config () {
    return {
      color: 'black',
      width: 500,
      height: 500,
      directed: true,
      node: {
        viewGenerator: (node) => {
          const retweetProb = this.state.retweetProbs[node.id];
          const isSelected = node.id === this.state.selected;
          const isRumor = this.state.retweeted.includes(node.id);
          const isOrigin = this.state.origin === node.id;
          return <CustomViewComponent
            node={node}
            isSelected={isSelected}
            isOrigin={isOrigin}
            retweetProb={retweetProb}
            isRumor={isRumor} />
        },
        fontSize: 14,
        fontColor: '#FFF',
        color: '#42b983',
      },
      link: {
        color: '#333',
      }
    }
  }
  componentDidMount() {
    this.getNetwork().then(network => {
      const data = {
        nodes: [],
        links: []
      }
      Object.keys(network).forEach(target => {
        data.nodes.push({ id: target });
        network[target].forEach(source => {
          data.links.push({ source, target });
        })
      });
      this.setState({ network, data, });
    })
  }
  getNetwork() {
    return fetch(`${api}/network.json`)
      .then(function(response) {
        return response.json();
      })
  }
  retweetProb(username, tweet) {
    const { retweeted } = this.state;
    const relevantLinks = this.state.data.links.filter(data => (
      (data.source === username) && !retweeted.includes(data.target)
    ));
    return Promise.all(
      relevantLinks.map(({ source, target }) => (
        fetch(`${api}/retweet-prob`, {
            method: "POST", // *GET, POST, PUT, DELETE, etc.
            headers: {
                "Content-Type": "application/json",
                "Accept": "application/json",
            },
            body: JSON.stringify({ username: target, tweet })
        }).then(response => response.json()).then(result => {
          this.setState(({ retweetProbs }) => ({
            retweetProbs: {
              ...retweetProbs,
              [target]: result
            }
          }))
          return {
            ...result,
            username: target
          }
        }).catch(e => {
          console.error(e);
          return {};
        })
      ))
    ).then(results => {
      const { retweeted, isDeterministic } = this.state;
      const newReweeted = retweeted.concat(results
        .filter(({ retweet_probability }) => (
          isDeterministic ?
            retweet_probability > 1 :
            retweet_probability > Math.random()
        ))
        .map(({ username }) => username));
      this.setState({ retweeted: newReweeted })
      return Promise.all(newReweeted
        .filter(username => !retweeted.includes(username))
        .map(username => this.retweetProb(username, tweet))
      );
    });
  }
  render() {
    const {
      data, retweetProbs, selected, pendingTweet, tweet,
      isDeterministic, isViewingInstructions
    } = this.state;
    return (
      <div className='network'>
        <div className='network__pane'>
          <Graph
              ref={this.graph}
              id='graph-id'
              data={data}
              onClickNode={(node) => {
                this.setState(({ selected }) => ({ selected: node, }));
              }}
              config={this.config()} />
          <div className='network__info network__info--vertical' hidden={!isViewingInstructions}>
            <button onClick={() => this.setState({ isViewingInstructions: false })}>
              Go to Simulator
            </button>
            <Instructions />
          </div>
          <div className='network__info network__info--vertical' hidden={isViewingInstructions}>
            <button onClick={() => this.setState({ isViewingInstructions: true })}>
              View Instructions
            </button>
            <div>
              <h2>
                {selected ? "Selected: @" + selected : ""}
              </h2>
              <textarea
                value={this.state.pendingTweet}
                onChange={(e) => this.setState({ pendingTweet: e.target.value })}
                rows="3"/>
              <div>
                <div>
                  <input
                    id='checkbox'
                    type='checkbox'
                    checked={isDeterministic}
                    onChange={(e) => {
                      this.setState(({ isDeterministic}) => ({ isDeterministic: !isDeterministic }))
                    }}/>
                  <label htmlFor='checkbox'>Deterministic</label>
                </div>
                <div>
                  <button onClick={() => {
                      this.setState(({ selected}) => ({
                        retweeted: [],
                        retweetProbs: {},
                        tweet: pendingTweet,
                        origin: selected
                      }), () => {
                        this.retweetProb(selected, pendingTweet);
                      });
                    }}>Simulate</button>
                </div>
              </div>
              <h2>
                Origin: {this.state.origin ?  '@' + this.state.origin : ""}
              </h2>
            </div>
            <div>
              <pre>
                  {retweetProbs[selected] ? "For tweet \"" + tweet + "\"\n\n" : ""}
                  {JSON.stringify(retweetProbs[selected], null, 4)}
              </pre>
            </div>
          </div>
        </div>
      </div>
    );
  }
}
