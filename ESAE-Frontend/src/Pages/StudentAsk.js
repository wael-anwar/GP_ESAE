import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './StudentAsk.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';
class StudentAsk extends Component {

 
    render() {
        return (
        <div>
    <Container style={{width:'660px',height:'590px',backgroundColor:'white'}}>
        <br />
    <Form style={{backgroundColor:'white'}}>

  <Form.Group  id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Form.Control id="TextEssay" as="textarea" placeholder="Enter Your Essay Question" />
   <br />
    <Button  style={{float:'right'}} variant="success" >Get Answer</Button>

  </Form.Group>

</Form>

 </Container>
            
          </div>
        );
    }
}

export default StudentAsk;
