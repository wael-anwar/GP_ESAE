import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import './signin.css';

class SignInForm extends Component {
    render() {
      const instructor="instructor";
      const student="student";
      const instructor_up = `/#/sign-up?${new URLSearchParams({instructor}).toString()}`;
      const student_up = `/#/sign-up?${new URLSearchParams({student}).toString()}`;
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      var name = "";
      if(params.get('student'))
      {
        name=params.get('student')
        
      }
      else if (params.get('instructor'))
      {
        name=params.get('instructor')
        
      }
      var href1="";
      if (name=="student")
      {
        href1=student_up;
      }
      else if (name=="instructor")
      {
        href1=instructor_up
      }
      else
      {
        href1="#/sign-up";
      }
        return (
          <form className="signin-forum-container" action method="post">
          <h1>Sign In</h1><br />
          <input type="text" name="email" id="email" placeholder="Email" /><br />
          <input type="password" name="password" id="password" placeholder="Password" /><br />
          <a href="#">Forgot Your Password?</a><br />
          <input type="submit" defaultValue="Sign In" /><br />
          <a href={href1}>Not a member? Sign up now!</a>
        </form>
        );
    }
}

export default SignInForm;
