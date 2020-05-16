import React, { Component } from 'react';
import {
  Container,
  Item,
  Grid,
  Menu,
  Pagination,
} from 'semantic-ui-react'

import '../stylesheets/App.css';
import Question from './Question';
import Search from './Search';
import $ from 'jquery';

class QuestionView extends Component {
  constructor(){
    super();
    this.state = {
      questions: [],
      page: 1,
      totalQuestions: 0,
      categories: {},
      currentCategory: null,
    }
  }

  componentDidMount() {
    this.getQuestions();
  }

  getQuestions = () => {
    $.ajax({
      url: `/questions?page=${this.state.page}`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          categories: result.categories,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  selectPage(num) {
    this.setState({page: num}, () => this.getQuestions());
  }

  getByCategory= (id) => {
    $.ajax({
      url: `/categories/${id}/questions`, //TODO: update request URL
      type: "GET",
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  onPageChange = (event, data) => {
    this.selectPage(data.activePage)
  }

  submitSearch = (searchTerm) => {
    $.ajax({
      url: `/questions`, //TODO: update request URL
      type: "POST",
      dataType: 'json',
      contentType: 'application/json',
      data: JSON.stringify({searchTerm: searchTerm}),
      xhrFields: {
        withCredentials: true
      },
      crossDomain: true,
      success: (result) => {
        this.setState({
          questions: result.questions,
          totalQuestions: result.total_questions,
          currentCategory: result.current_category })
        return;
      },
      error: (error) => {
        alert('Unable to load questions. Please try your request again')
        return;
      }
    })
  }

  questionAction = (id) => (action) => {
    if(action === 'DELETE') {
      if(window.confirm('are you sure you want to delete the question?')) {
        $.ajax({
          url: `/questions/${id}`, //TODO: update request URL
          type: "DELETE",
          success: (result) => {
            this.getQuestions();
          },
          error: (error) => {
            alert('Unable to load questions. Please try your request again')
            return;
          }
        })
      }
    }
  }

  render() {
    const { currentCategory } = this.state
    return (
      <Container>
        <Grid className="question-view">
          <Grid.Row>
            <Grid.Column mobile={16} tablet={6} widescreen={4} largeScreen={4} className="categories-list">
              <h2 onClick={() => {this.getQuestions()}}>Categories</h2>
              <Menu pointing vertical id="categories">
                {Object.keys(this.state.categories).map((id) => (
                  <Menu.Item
                    key={id}
                    active={currentCategory === +id}
                    onClick={() => {this.getByCategory(id)}}
                  >
                    <img className="category" src={`${this.state.categories[id]}.svg`} alt={this.state.categories[id]} />
                    {this.state.categories[id]}
                  </Menu.Item>
                ))}
              </Menu>
              <Search submitSearch={this.submitSearch}/>
            </Grid.Column>
            <Grid.Column mobile={16} tablet={10} widescreen={12} largeScreen={12} className="questions-list">
              <h2>Questions</h2>
              <Item.Group divided>
              {this.state.questions.map((q, ind) => (
                <Question
                key={q.id}
                question={q.question}
                answer={q.answer}
                category={this.state.categories[q.category]}
                difficulty={q.difficulty}
                questionAction={this.questionAction(q.id)}
                />
                ))}
              </Item.Group>
              <Pagination
                defaultActivePage={this.state.page}
                totalPages={Math.ceil(this.state.totalQuestions / 10)}
                onPageChange={this.onPageChange}
              />
            </Grid.Column>
          </Grid.Row>
        </Grid>
      </Container>
    );
  }
}

export default QuestionView;
