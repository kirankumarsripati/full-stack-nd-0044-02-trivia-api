import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import {
  Menu,
  Image,
} from 'semantic-ui-react'
import '../stylesheets/Header.css';

class Header extends Component {

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    return (
      <Menu borderless>
        <Menu.Item onClick={() => {this.navTo('')}}>
          <Image size='mini' src='/paper.svg' />
        </Menu.Item>
        <Menu.Item header onClick={() => {this.navTo('')}}>Udacitrivia</Menu.Item>
        <Menu.Item as={ NavLink } to="/" exact>List</Menu.Item>
        <Menu.Item as={ NavLink } to="/add">Add</Menu.Item>
        <Menu.Item as={ NavLink } to="/play">Play</Menu.Item>
      </Menu>
    );
  }
}

export default Header;
