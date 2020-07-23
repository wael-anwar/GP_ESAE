import React, { Component } from 'react';
import { HashRouter as Router, Route} from 'react-router-dom';
import SignUpForm from './Pages/SignUpForm';
import SignInForm from './Pages/SignInForm';
import Homepage from './Pages/Homepage';
import InstructorHome from './Pages/InstructorHome';
import CreateExam from './Pages/CreateExam';
import FromExisting from './Pages/FromExisting';
import ViewExams from './Pages/ViewExams';
import ViewEdit from './Pages/ViewEdit';
import ViewGrade from './Pages/ViewGrade';
import EditMCQ from './Pages/EditMCQ';
import EditTF from './Pages/EditTF';
import EditComplete from './Pages/EditComplete';
import EditEssay from './Pages/EditEssay';
import TakeExam from './Pages/TakeExam';
import StudentHome from './Pages/StudentHome';
import StudentAsk from './Pages/StudentAsk';
import StudentExams from './Pages/StudentExams';
import Exam from './Pages/Exam';
import ViewEditExam from './Pages/ViewEditExam';
import './App.css';
import { Container } from '@material-ui/core';
import 'bootstrap/dist/css/bootstrap.min.css';
import Navbar from 'react-bootstrap/Navbar';
import Nav from 'react-bootstrap/Nav';
//import Form from 'react-bootstrap/Form';
//import FormControl from 'react-bootstrap/FormControl';
//import Button from 'react-bootstrap/Button';
class App extends Component {
  render() {
    return (
      
      <Router basename="/esae-frontend/">
       <Container fixed>
          <Navbar fixed="top" bg="dark" variant="dark">
        <Navbar.Brand href="#/home">E.S.A.E</Navbar.Brand>
        <Nav className="mr-auto">
          <Nav.Link href="#/home">Home</Nav.Link>

        </Nav>
      </Navbar>
       </Container>
              <Route exact path="/home" component={Homepage}>
              </Route>
              <Route exact path="/" component={Homepage}>
              </Route>
              <Route path="/sign-up" component={SignUpForm}>
              </Route>
              <Route path="/sign-in" component={SignInForm}>
              </Route>
              <Route path="/instructor-home" component={InstructorHome}>
              </Route>
              <Route path="/instructor-create" component={CreateExam}>
              </Route>
			        <Route path="/instructor-from-exist" component={FromExisting}>
              </Route>
              <Route path="/instructor-view-all" component={ViewExams}>
              </Route>
			        <Route path="/instructor-view-edit" component={ViewEdit}>
              </Route>
              <Route path="/instructor-view-grade" component={ ViewGrade}>
              </Route>
              <Route path="/instructor-view-edit-exam" component={ViewEditExam}>
              </Route>
              <Route path="/instructor-exam" component={Exam}>
              </Route>
			        <Route path="/instructor-edit-mcq" component={EditMCQ}>
              </Route>
              <Route path="/instructor-edit-tf" component={EditTF}>
              </Route>
              <Route path="/instructor-edit-complete" component={EditComplete}>
              </Route>
              <Route path="/instructor-edit-essay" component={EditEssay}>
              </Route>
              <Route path="/student-home" component={StudentHome}>
              </Route>
              <Route path="/student-ask" component={StudentAsk}>
              </Route>
              <Route path="/student-view-all" component={StudentExams}>
              </Route>
              <Route path="/student-take-exam" component={TakeExam}>
              </Route>
    
      </Router>
    );
  }
}

export default App;
