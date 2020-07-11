import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import Modal from 'react-bootstrap/Modal'
import Button from 'react-bootstrap/Button';



class SignUpForm extends Component {

    constructor(props) {
      super(props);
      this.state = {value: '', SignUpResult:null};

    }

    async Authenticate(Identity, UserName, Name, Password)
    {
      const response = await fetch('/SignUpStudentInstructor/'+Identity+'/'+UserName+'/'+Name+'/'+Password).then(response => response.json());
      this.setState({SignUpResult:response.SignIn});
    }
    async SignUpStudentInstructor(UserName, Name, Password)
    {
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
      await this.Authenticate(Identity, UserName, Name, Password)
      if (this.state.SignUpResult == "Added successfully")
      {
        document.getElementById('SignupFinish').style.display='block';
      }
      else if (this.state.SignUpResult == "Error")
      {
        alert("Unsuccessful process, please try again. ")
      }
      
    }


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
          <div>

            <div style={{display:'none'}} class="modal-custom" id="SignupFinish">
            <Modal.Dialog  >
                <Modal.Header >
                <Modal.Title>Sign Up Process</Modal.Title>
                </Modal.Header>
                <Modal.Body>
                  Welcome {window.Name}, you have successfully signed up, now please login with your credentials
              </Modal.Body>
              <Modal.Footer>
                <Button variant="primary" onClick={event =>  window.location.href='#/'} >Ok</Button>
              </Modal.Footer>
            </Modal.Dialog>
            </div>


            <form className="signin-forum-container">
              <h1>Sign Up</h1><br />
              <input type="text" name="name" id="name" placeholder="Name" /><br />
              <input type="text" name="username" id="username" placeholder="User Name [must be unique]" /><br />
              <input type="password" name="password" id="password" placeholder="Password" /><br />
              
              <input type="submit" defaultValue="Sign Up" 
              onClick={()=>{this.SignUpStudentInstructor(document.getElementById('username').value, document.getElementById('name').value,
              document.getElementById('password').value)}} /><br />
              <a href={href1}>Already a member? Sign in now!</a>
            </form>
          </div>
        );
    }
}

export default SignUpForm;
