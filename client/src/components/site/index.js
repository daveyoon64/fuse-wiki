import React, { Component } from 'react';
import Form from './form';
import Links from './links';

export default class extends Component {
  state = {
    isLoading: false,
    links: null,
    error: false,
    sourceVal: "",
    targetVal: ""
  }

  getLinks = async (e) => {
    e.preventDefault();

    fetch('https://api.fuse.wiki/v1/generate_link',
    {
      method: 'post',
      headers: {
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({raw_source_title: this.state.sourceVal, raw_target_title: this.state.targetVal})
    })
      .then( res => res.json())
      .then( res => {
        console.log(res)
        this.setState({links: res.result, isLoading: false});
      })
      .catch( err => {
        this.setState({error: true, isLoading: false});
        console.log(err);
      })

    this.setState({isLoading: true});
  }

  sourceChange = async (e) => {
    e.preventDefault();
    this.setState({sourceVal: e.target.value})
  }

  targetChange = async (e) => {
    e.preventDefault();
    this.setState({targetVal: e.target.value})
  }

  render() {
    return (
      <div className="ui center aligned container">
        <h1 className="ui huge inverted header">Welcome to fuse.wiki</h1>
        <Form
          getLinks={this.getLinks}
          isLoading={this.state.isLoading}
          sourceVal={this.state.sourceVal}
          targetVal={this.state.targetVal}
          sourceChange={this.sourceChange}
          targetChange={this.targetChange}
        />
        {this.state.links ? <Links links={this.state.links[0]} /> : <h1 className="ui inverted header">Please enter values</h1>}
        </div>
    );
  }
}