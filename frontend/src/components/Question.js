import React, { Component } from 'react';
import {
  Button,
  Icon,
  Item,
  Label,
} from 'semantic-ui-react'

import '../stylesheets/Question.css';

class Question extends Component {
  constructor(){
    super();
    this.state = {
      visibleAnswer: false
    }
  }

  flipVisibility() {
    this.setState({visibleAnswer: !this.state.visibleAnswer});
  }

  render() {
    const { question, answer, category, difficulty } = this.props;
    return (
      <Item>
        <Item.Content>
          <Item.Header>{question}</Item.Header>
          <Item.Description as='h2'
            style={{"display": this.state.visibleAnswer ? 'block' : 'none'}}>
              Answer: {answer}
          </Item.Description>
          <Item.Extra>
            <Label>
              <img
                src={`${category}.svg`}
                alt={category}
              />
              {category}
            </Label>
            <Label>Difficulty: {difficulty}</Label>
            <Button basic color='red' floated='right' onClick={() => this.props.questionAction('DELETE')}>
              <Icon name="trash alternate outline" /> Delete
            </Button>
            <Button primary floated='right'
              onClick={() => this.flipVisibility()}>
              {this.state.visibleAnswer ? 'Hide' : 'Show'} Answer
            </Button>
          </Item.Extra>
        </Item.Content>
      </Item>
    );
  }
}

export default Question;
