import React, { Component } from 'react';
import { NavLink } from 'react-router-dom'
import {
  Icon,
  Image,
  Menu,
  Responsive,
  Sidebar,
} from 'semantic-ui-react'
import '../stylesheets/Header.css';

const getWidth = () => {
  const isSSR = typeof window === 'undefined'

  return isSSR ? Responsive.onlyTablet.minWidth : window.innerWidth
}

class Header extends Component {
  state = {}

  handleSidebarHide = () => this.setState({ sidebarOpened: false })

  handleToggle = () => this.setState({ sidebarOpened: true })

  navTo(uri){
    window.location.href = window.location.origin + uri;
  }

  render() {
    const { sidebarOpened } = this.state
    return (
      <>
      <Menu borderless>
        <Menu.Item onClick={() => {this.navTo('')}}>
          <Image size='mini' src='/paper.svg' />
        </Menu.Item>
        <Menu.Item header onClick={() => {this.navTo('')}}>Udacitrivia</Menu.Item>
        <Responsive className='menu' getWidth={getWidth} minWidth={Responsive.onlyTablet.minWidth}>
          <Menu.Item as={ NavLink } to="/" exact>List</Menu.Item>
          <Menu.Item as={ NavLink } to="/add">Add</Menu.Item>
          <Menu.Item as={ NavLink } to="/play">Play</Menu.Item>
        </Responsive>
        <Menu.Item as={ Responsive }
          onClick={this.handleToggle}
          position='right'
          getWidth={getWidth}
          maxWidth={Responsive.onlyMobile.maxWidth}
        >
          <Icon name='sidebar' />
        </Menu.Item>
      </Menu>

      <Responsive
        getWidth={getWidth}
        maxWidth={Responsive.onlyMobile.maxWidth}
        >
        <Sidebar
          as={Menu}
          animation='overlay'
          inverted
          onHide={this.handleSidebarHide}
          vertical
          visible={sidebarOpened}
        >
          <Menu.Item as={ NavLink } to="/" exact>List</Menu.Item>
          <Menu.Item as={ NavLink } to="/add">Add</Menu.Item>
          <Menu.Item as={ NavLink } to="/play">Play</Menu.Item>
        </Sidebar>
      </Responsive>
      </>
    );
  }
}

export default Header;
