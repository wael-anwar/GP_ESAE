import React, { Component } from 'react';
import { HashRouter as Router, Route, Link, NavLink } from 'react-router-dom';
import SignUpForm from './Pages/SignUpForm';
import SignInForm from './Pages/SignInForm';
import Homepage from './Pages/Homepage';
import InstructorHome from './Pages/InstructorHome';
import CreateExam from './Pages/CreateExam';
import Popup from './Pages/Popup';
import ViewExams from './Pages/ViewExams';
import StudentHome from './Pages/StudentHome';
import StudentAsk from './Pages/StudentAsk';
import StudentExams from './Pages/StudentExams';
import Exam from './Pages/Exam';
import './App.css';
import { Container } from '@material-ui/core';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
import Form from 'react-bootstrap/Form';
import FormControl from 'react-bootstrap/FormControl';
import Button from 'react-bootstrap/Button';
class App extends Component {
  render() {
    return (
      
      <Router basename="/esae-frontend/">
       <Container fixed>
          <Navbar fixed="top" bg="dark" variant="dark">
        <Navbar.Brand href="#home">E.S.A.E</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="#home">Home</Nav.Link>

        </Nav>
        <Form inline>
          <FormControl type="text" placeholder="Search" className="mr-sm-2" />
          <Button variant="outline-info">Search</Button>
        </Form>
      </Navbar>
       </Container>
              <Route exact path="/home" component={Homepage}>
              </Route>
              <Route path="/sign-up" component={SignUpForm}>
              </Route>
              <Route path="/sign-in" component={SignInForm}>
              </Route>
              <Route path="/instructor-home" component={InstructorHome}>
              </Route>
              <Route path="/instructor-create" component={CreateExam}>
              </Route>
              <Route path="/instructor-view-all" component={ViewExams}>
              </Route>
              <Route path="/instructor-exam" component={Exam}>
              </Route>
              <Route path="/student-home" component={StudentHome}>
              </Route>
              <Route path="/student-ask" component={StudentAsk}>
              </Route>
              <Route path="/student-view-all" component={StudentExams}>
              </Route>
        
      </Router>
    );
  }
}

export default App;
