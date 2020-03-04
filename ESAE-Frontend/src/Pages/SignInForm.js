import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import './signin.css';

class SignInForm extends Component {
    render() {
        return (
          <form className="signin-forum-container" action method="post">
          <h1>Sign In</h1><br />
          <input type="text" name="email" id="email" placeholder="Email" /><br />
          <input type="password" name="password" id="password" placeholder="Password" /><br />
          <a href="#">Forgot Your Password?</a><br />
          <input type="submit" defaultValue="Sign In" /><br />
          <a href="#/esae-frontend/sign-up">Not a member? Sign up now!</a>
        </form>
        );
    }
}

export default SignInForm;
