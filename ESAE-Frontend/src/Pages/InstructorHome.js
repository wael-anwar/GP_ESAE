import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './InstructorHome.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class InstructorHome extends Component {
handleCreate()
{
    if (document.getElementById('BtnNew').style.display=='block'||document.getElementById('BtnExist').style.display=='block')
    {
        document.getElementById('BtnNew').style.display='none';
        document.getElementById('BtnExist').style.display='none';
    }
    else
    {
        document.getElementById('BtnNew').style.display='block';
        document.getElementById('BtnExist').style.display='block';
    }
}
    render() {
        return (
        <div>
          
          <h1>Welcome Dr. Magda Fayek</h1>
    <br />
    <Container>
     <Row style={{ justifyContent:'space-evenly'}}>
         <Col ><Button onClick={this.handleCreate} size="lg"variant="primary">Create Exam</Button></Col>
        <Col  ><Button href="#/instructor-view-all" size="lg" variant="primary">View Exams</Button></Col>
         <Col  ><Button href="#/instructor-view-edit" size="lg"variant="primary">Edit Exam</Button></Col>
         <Col  ><Button href="#/instructor-view-grade" size="lg"variant="primary">Grade Exam</Button></Col>
     </Row>
     <Row style={{width:'17%'}}>
        
         <Col ><Button id="BtnNew"style={{display:'none'}} href="#/instructor-create" size="sm"variant="primary">New Exam</Button></Col>
       
     </Row>
     <Row style={{width:'17%'}}>
        
        <Col ><Button id="BtnExist" style={{display:'none'}} href="#/instructor-from-exist" size="sm"variant="primary">From Existing Exams</Button></Col>
    </Row>


 </Container>
            
          </div>
        );
    }
}

export default InstructorHome;
