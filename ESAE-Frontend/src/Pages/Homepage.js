import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './homestyle.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class Homepage extends Component {
  
    render() {
        return (
        <div>
 <h1>Welcome to Exam Solver and Evaluator</h1>
           <br />
           <Container>
            <Row style={{ justifyContent:'space-evenly'}}>
                <Col style={{flexGrow:'unset'}}  >
                <Card bg="light" style={{ width: '13rem' }}>
            <Card.Img variant="top" src={require('./student.png')} />
            <Card.Body style={{ textAlign:'center'}}>
                <Card.Title>I'm a Student</Card.Title>
                <Card.Text>
                Now you can Get Question's Answers with One Click
                </Card.Text>
                <Button href="#/student-home" size="lg" variant="success">Join Now!</Button>
            </Card.Body>
            </Card></Col>
                <Col style={{flexGrow:'unset'}} ><Card bg="light" style={{ width: '13rem' }}>
            <Card.Img variant="top" src={require('./instructor.png')} />
            <Card.Body style={{ textAlign:'center'}}>
                <Card.Title>I'm an Instructor</Card.Title>
                <Card.Text>
                Now you Form your Exam and Evaluate it with One Click
                </Card.Text>
                <Button href="#/instructor-home" size="lg" variant="danger">Join Now!</Button>
            </Card.Body>
            </Card></Col>
            </Row>

        </Container>
        
        

            
          </div>
        );
    }
}

export default Homepage;
