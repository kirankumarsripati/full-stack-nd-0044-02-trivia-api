import React, { Component } from 'react';
import {
  Button,
  Container,
  Form,
} from 'semantic-ui-react'
import $ from 'jquery';

import '../stylesheets/FormView.css';

const difficultyOptions = [
  { key: '1', value: '1', text: '1' },
  { key: '2', value: '2', text: '2' },
  { key: '3', value: '3', text: '3' },
  { key: '4', value: '4', text: '4' },
  { key: '5', value: '5', text: '5' },
]

class FormView extends Component {
  constructor(props){
    super();
    this.state = {
      question: "",
      answer: "",
      difficulty: 1,
      category: 1,
      categories: {},
      categoriesSelect: [],
    }
  }

  componentDidMount(){
    $.ajax({
      url: `/categories`, //DONE: update request URL
      type: "GET",
      success: (result) => {
        const categories = result.categories;
        const categoryOptions = Object.keys(categories).map((id) => {
          return { key: id, value: id, text: categories[id] }
        })
        this.setState({
          categories: result.categories,
          categoryOptions,
        })
        return;
      },
      error: (error) => {
        alert('Unable to load categories. Please try your request again')
        return;
      }
    })
  }


  submitQuestion = (event) => {
    event.preventDefault();
    $.ajax({
      url: '/questions', //DONE: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({
        question: this.state.question,
        answer: this.state.answer,
        difficulty: this.state.difficulty,
        category: this.state.category
      }),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        document.getElementById("add-question-form").reset();
        return;
      },
      error: (error) => {
        alert('Unable to add question. Please try your request again')
        return;
      }
    })
  }

  handleChange = (event) => {
    this.setState({[event.target.name]: event.target.value})
  }

  render() {
    return (
      <Container id="add-form">
        <h2>Add a New Trivia Question</h2>
        <Form id="add-question-form" onSubmit={this.submitQuestion}>
          <Form.Field>
            <label>
              Question
              <input type="text" name="question" onChange={this.handleChange}/>
            </label>
          </Form.Field>
          <Form.Field>
            <label>
              Answer
              <input type="text" name="answer" onChange={this.handleChange}/>
            </label>
          </Form.Field>
          <Form.Group widths='equal'>
            <Form.Select
              onChange={this.handleChange}
              fluid
              label='Difficulty'
              name="difficulty"
              options={difficultyOptions}
              placeholder='Difficulty'
            />
            { this.state.categoryOptions &&
            <Form.Select
              onChange={this.handleChange}
              fluid
              label='Category'
              name="category"
              options={this.state.categoryOptions}
              placeholder='Category'
            />}
          </Form.Group>
          <Button type='submit'>Submit</Button>
        </Form>
      </Container>
    );
  }
}

export default FormView;
