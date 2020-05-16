import React, { Component } from 'react';
import {
  Button,
  Container,
  Form,
  Menu,
} from 'semantic-ui-react'
import $ from 'jquery';

import '../stylesheets/QuizView.css';

const questionsPerPlay = 5;

class QuizView extends Component {
  constructor(props){
    super();
    this.state = {
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      categories: {},
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
  }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //DONE: update request URL
      type: "GET",
      success: (result) => {
        this.setState({ categories: result.categories })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }

  selectCategory = ({type, id=0}) => {
    this.setState({quizCategory: {type, id}}, this.getNextQuestion)
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  getNextQuestion = () => {
    const previousQuestions = [...this.state.previousQuestions]
    if(this.state.currentQuestion.id) { previousQuestions.push(this.state.currentQuestion.id) }

    $.ajax({
      url: '/quizzes', //DONE: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        previous_questions: previousQuestions,
        quiz_category: this.state.quizCategory
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          showAnswer: false,
          previousQuestions: previousQuestions,
          currentQuestion: result.question,
          guess: '',
          forceEnd: result.question ? false : true
        })
        return;
      },
      error: (error) => {
        alert('Unable to load question. Please try your request again')
        return;
      }
    })
  }

  submitGuess = (event) => {
    event.preventDefault();
    let evaluate =  this.evaluateAnswer()
    this.setState({
      numCorrect: !evaluate ? this.state.numCorrect : this.state.numCorrect + 1,
      showAnswer: true,
    })
  }

  restartGame = () => {
    this.setState({
      quizCategory: null,
      previousQuestions: [],
      showAnswer: false,
      numCorrect: 0,
      currentQuestion: {},
      guess: '',
      forceEnd: false
    })
  }

  renderPrePlay(){
    return (
      <Container className="center aligned">
        <h2>Choose Category</h2>
        <Menu pointing vertical className="menu-center">
          <Menu.Item onClick={this.selectCategory}>ALL</Menu.Item>
          {Object.keys(this.state.categories).map((id) => (
            <Menu.Item
              key={id}
              onClick={() => {this.selectCategory({type: this.state.categories[id], id})}}
            >
              <img className="category" src={`${this.state.categories[id]}.svg`} alt={this.state.categories[id]} />
              {this.state.categories[id]}
            </Menu.Item>
          ))}
        </Menu>
      </Container>
    )
  }

  renderFinalScore(){
    return(
      <Container className="center aligned">
        <h2>Your Final Score is {this.state.numCorrect}</h2>
        <Button primary onClick={this.restartGame}> Play Again? </Button>
      </Container>
    )
  }

  evaluateAnswer = () => {
    // eslint-disable-next-line
    const formatGuess = this.state.guess.replace(/[.,\/#!$%\^&\*;:{}=\-_`~()]/g,"").toLowerCase()
    const answerArray = this.state.currentQuestion.answer.toLowerCase().split(' ');
    return answerArray.includes(formatGuess)
  }

  renderCorrectAnswer(){
    let evaluate =  this.evaluateAnswer()
    return(
      <Container className="center aligned">
        <h3>{this.state.currentQuestion.question}</h3>
        <div className={`${evaluate ? 'correct' : 'wrong'}`}>{evaluate ? "You were correct!" : "You were incorrect"}</div>
        <div className="quiz-answer">{this.state.currentQuestion.answer}</div>
        <Button primary onClick={this.getNextQuestion}> Next Question </Button>
      </Container>
    )
  }

  renderPlay(){
    return this.state.previousQuestions.length === questionsPerPlay || this.state.forceEnd
      ? this.renderFinalScore()
      : this.state.showAnswer
        ? this.renderCorrectAnswer()
        : (
          <Container className="center aligned">
            <h3>{this.state.currentQuestion.question}</h3>
            <Form onSubmit={this.submitGuess}>
              <Form.Field>
                <label>
                  Your Answer
                  <input className="answer-input" type="text" name="guess" onChange={this.handleChange}/>
                </label>
              </Form.Field>
              <Button primary type="submit">Submit Answer</Button>
            </Form>
          </Container>
        )
  }


  render() {
    return this.state.quizCategory
        ? this.renderPlay()
        : this.renderPrePlay()
  }
}

export default QuizView;
