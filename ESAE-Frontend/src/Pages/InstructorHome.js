import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './InstructorHome.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class InstructorHome extends Component {

    render() {
        return (
        <div>
          
          <h1>Welcome Dr.</h1>
    <br />
    <Container>
     <Row style={{ justifyContent:'space-evenly'}}>
         <Col ><Button href="#/instructor-create" size="lg"variant="primary">Create Exam</Button></Col>
         <Col  ><Button href="#/instructor-view-all" size="lg" variant="primary">View Exams</Button></Col>
         <Col  ><Button size="lg"variant="primary">Edit Exam</Button></Col>
         <Col  ><Button size="lg"variant="primary">Grade Exam</Button></Col>
     </Row>

 </Container>
            
          </div>
        );
    }
}

export default InstructorHome;
