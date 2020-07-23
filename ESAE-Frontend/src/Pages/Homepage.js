import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './homestyle.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class Homepage extends Component {
  
    render() {
        const instructor="instructor";
        const student="student";
        const instructor_up = `/#/sign-up?${new URLSearchParams({instructor}).toString()}`;
        const student_up = `/#/sign-up?${new URLSearchParams({student}).toString()}`;
        const instructor_in = `/#/sign-in?${new URLSearchParams({instructor}).toString()}`;
        const student_in = `/#/sign-in?${new URLSearchParams({student}).toString()}`;
        return (
        <div>
 <h1>Welcome to Exam Solver and Evaluator</h1>
           <Container style={{textAlign:'center'}}>
            <Row style={{ justifyContent:'space-around',display:'inline-flex'}}>
                <Col  >
                <Card bg="light" style={{ width: '15rem' }}>
            <Card.Img variant="top" src={require('./student.png')} />
            <Card.Body style={{ textAlign:'center'}}>
                <Card.Title>I'm a Student</Card.Title>
                <Card.Text>
                Now you can Get Question's Answers and Take Exams with One Click
                </Card.Text>
                
                <Button href={student_up} size="lg" variant="success">Join Now!</Button>
                <Button href={student_in} size="lg" variant="primary">Sign in!</Button>
            </Card.Body>
            </Card>
            </Col>
                <Col >
                <Card bg="light" style={{ width: '15rem' }}>
            <Card.Img variant="top" src={require('./instructor.png')} />
            <Card.Body style={{ textAlign:'center'}}>
                <Card.Title>I'm an Instructor</Card.Title>
                <Card.Text>
                Now you can Form your Exams and Evaluate it with One Click
                </Card.Text>
                <Button href={instructor_up} size="lg" variant="danger">Join Now!</Button>
                <Button href={instructor_in} size="lg" variant="primary">Sign in!</Button>
            </Card.Body>
            </Card>
            </Col>
            </Row>

        </Container>
        
        

            
          </div>
        );
    }
}

export default Homepage;
