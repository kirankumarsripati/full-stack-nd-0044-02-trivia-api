import React, { Component } from 'react'
import {
  Input,
  Button,
} from 'semantic-ui-react'


class Search extends Component {
  state = {
    query: '',
  }

  getInfo = (event) => {
    event.preventDefault();
    this.props.submitSearch(this.state.query)
  }

  handleInputChange = (event, data) => {
    this.setState({
      query: data.value
    })
  }

  render() {
    return (
      <form onSubmit={this.getInfo}>
        <Input
          placeholder='Search questions...'
          onChange={this.handleInputChange}
        />
        <Button className="search-btn" type="submit">Search</Button>
      </form>
    )
  }
}

export default Search
