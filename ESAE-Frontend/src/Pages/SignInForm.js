import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import './signin.css';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';



class SignInForm extends Component {

    constructor(props) {
      super(props);
      this.state = {value: '', SignInResult:null, Name:null, ID:null};
      window.IDToken=[];

    }

    async Authenticate(Identity, UserName, Password)
    {
      const response = await fetch('/SignInStudentInstructor/'+Identity+'/'+UserName+'/'+Password).then(response => response.json());
      this.setState({SignInResult:response.SignIn, ID:response.ID});
    }
    async SignInStudentInstructor(UserName, Password)
    {
      this.state.Name=UserName;
      var Identity = 0
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      if(params.get('student'))
      {
        Identity='student'
      }
      else if (params.get('instructor'))
      {
        Identity='instructor'
      }
      await this.Authenticate(Identity, UserName, Password)
      //globalThis.window.IDToken=this.state.ID
      //Object.freeze(globalThis.window.IDToken)
      window.IDToken = this.state.ID
      if (this.state.SignInResult == "Found")
      {
        document.getElementById('SigninFinish').style.display='block';
        
      }
      else if (this.state.SignInResult == "Error")
      {
        alert("Invalid credentials")
      }
      
      
    }

    RouteAfterSignIn()
    {

    }
    render() {
      const instructor="instructor";
      const student="student";
      const instructor_up = `/#/sign-up?${new URLSearchParams({instructor}).toString()}`;
      const student_up = `/#/sign-up?${new URLSearchParams({student}).toString()}`;
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      var name = "";
      var home = "";
      if(params.get('student'))
      {
        name=params.get('student')
        window.Name=this.state.Name
        var username=this.state.Name
        //alert(username)
        home = `#/student-home?${new URLSearchParams({username}).toString()}`;
      }
      else if (params.get('instructor'))
      {
        name=params.get('instructor')
        window.Name=this.state.Name
        var username=this.state.Name
        var IDToken = this.state.ID
        home = `#/instructor-home?${new URLSearchParams({username,IDToken}).toString()}`;
        
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
          <div>
            <div style={{display:'none'}} class="modal-custom" id="SigninFinish">
            <Modal.Dialog  >
                <Modal.Header >
                <Modal.Title>Authentication</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  Welcome {window.Name} you have been successfully authenticated
              </Modal.Body>
              <Modal.Footer>
                <Button variant="primary" onClick={event =>  window.location.href=home} >Ok</Button>
              </Modal.Footer>
            </Modal.Dialog>
            </div>
            <form className="signin-forum-container" >
            <h1>Sign In</h1><br />
            <input type="text" name="username" id="username" placeholder="User Name" /><br />
            <input type="password" name="password" id="password" placeholder="Password" /><br />
            <a href="#">Forgot Your Password?</a><br />
            <input type="submit" defaultValue="Sign In" 
            onClick={()=>{this.SignInStudentInstructor(document.getElementById('username').value, document.getElementById('password').value)}} /><br />
            <a href={href1}>Not a member? Sign up now!</a>
          </form>
          </div>
          
        );
    }
}

export default SignInForm;
