import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
class SignUpForm extends Component {

    render() {
      const instructor="instructor";
      const student="student";
      const instructor_in = `/#/sign-in?${new URLSearchParams({instructor}).toString()}`;
      const student_in = `/#/sign-in?${new URLSearchParams({student}).toString()}`;
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
        href1=student_in;
      }
      else if (name=="instructor")
      {
        href1=instructor_in
      }
      else
      {
        href1="#/sign-in";
      }
        return (
          <form className="signin-forum-container" action method="post">
          <h1>Sign Up</h1><br />
          <input type="text" name="username" id="username" placeholder="Name" /><br />
          <input type="text" name="email" id="email" placeholder="Email" /><br />
          <input type="password" name="password" id="password" placeholder="Password" /><br />
          
          <input type="submit" defaultValue="Sign Up" /><br />
          <a href={href1}>Already a member? Sign in now!</a>
        </form>
        );
    }
}

export default SignUpForm;
