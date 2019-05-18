import React from 'react';
import api from './api';
import './Instructions.css';


export default class Instructions extends React.Component {
  render() {
    const link = `${api}/report.pdf`;
    return (
      <div className='instructions'>
        <h1>Instructuctions</h1>
        <p>
          This app simulates a twitter network. Each of the 20 users present is a real twitter user, and all predictions this app will make are based on the user's prior history of tweets. To use this app, select a node in the app by clicking on it. Then enter a tweet you would like to simulate the user making. If the deterministic button is checked, the result will be the same every time the app is run. If the deterministc button is not checked, the results will be based on the probability of a tweet being classified as retweeted or not retweeted and will not be deterministic.
        </p>
        <p>
          The color of a user after a tweet is sent out is based on the liklihood of a tweet being retweeted vs the average likelihood. If a tweet is more likely to be retweeted than average, the tweet will be a shade of blue. The darker the shade of blue, the more likely the chance of a retweet. If a tweet is less likely to be retweeted than average, the tweet will be a shade of red. The darker the shade of red, the less likely the chance of a retweet. When a tweet is actually retweeted by a user, the shape of the node will change from a square to a circle. In order to view details about why a particular user retweeted or did not retweet a given tweet, you can select the given user. Only users directly adjacent to users who have tweeted or retweeted will have this information available.
        </p>
        <p>
          The paper associated with this project that explains the algorithm used can be found <a href={link}>here.</a> A github repo containing the code for this project can be found <a href='https://www.github.com/didericis/twitter-rumor-spreader.git'>here</a>.
        </p>
      </div>
    );
  }
}
