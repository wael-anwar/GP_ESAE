import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
class SignUpForm extends Component {

    render() {
        return (
          <form className="signin-forum-container" action method="post">
          <h1>Sign Up</h1><br />
          <input type="text" name="username" id="username" placeholder="Name" /><br />
          <input type="text" name="email" id="email" placeholder="Email" /><br />
          <input type="password" name="password" id="password" placeholder="Password" /><br />
          
          <input type="submit" defaultValue="Sign Up" /><br />
          <a href="#/esae-frontend/sign-in">Already a member? Sign in now!</a>
        </form>
        );
    }
}

export default SignUpForm;
