import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './StudentHome.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class StudentHome extends Component {

    render() {
        return (
        <div>
          
          <h1>Welcome ya Taleb.</h1>
    <br />
    <Container style={{ justifyContent:'center'}}>
     <Row style={{ justifyContent:'space-evenly'}}>
         <Col  style={{ flexGrow:'unset'}}><Button style={{width: 'max-content'}} href="#/student-ask" size="lg"variant="primary">Ask a Question</Button></Col>
         <Col style={{ flexGrow:'unset'}} ><Button style={{width: 'max-content'}} href="#/student-view-all" size="lg" variant="primary">Take Exam</Button></Col>
     </Row>

 </Container>
            
          </div>
        );
    }
}

export default StudentHome;
