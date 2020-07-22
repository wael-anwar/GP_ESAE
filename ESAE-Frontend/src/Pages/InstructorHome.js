import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './InstructorHome.css';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import './SignInForm';

class InstructorHome extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', fullname:null, id:null};
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const username=params.get('username')
        const IDToken=params.get('IDToken')
        this.state.id=IDToken
        //alert(this.state.id)
        this.GetName(username)
        
  
    }

    GetName(username)
    {
      fetch('/GetInstName/'+username)
        .then(response => response.json())
        .then(data => this.setState({fullname : data.name}));
    }

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
        const IDToken = this.state.id;
        const href1 = `/#/instructor-view-all?${new URLSearchParams({IDToken}).toString()}`;
        const href2 = `/#/instructor-view-edit?${new URLSearchParams({IDToken}).toString()}`;
        const href3 = `/#/instructor-view-grade?${new URLSearchParams({IDToken}).toString()}`;
        const href4 = `/#/instructor-create?${new URLSearchParams({IDToken}).toString()}`;
        const href5 = `/#/instructor-from-exist?${new URLSearchParams({IDToken}).toString()}`;
        return (
        <div>
          
          <h1>Welcome {this.state.fullname}</h1>
    <br />
    <Container>
     <Row style={{ justifyContent:'space-evenly'}}>
         <Col ><Button onClick={this.handleCreate} size="lg"variant="primary">Create Exam</Button></Col>
        <Col  ><Button href={href1} size="lg" variant="primary">View Exams</Button></Col>
         <Col  ><Button href={href2} size="lg"variant="primary">Edit Exam</Button></Col>
         <Col  ><Button href={href3} size="lg"variant="primary">Grade Exam</Button></Col>
     </Row>
     <Row style={{width:'17%'}}>
        
         <Col ><Button id="BtnNew"style={{display:'none'}} href={href4} size="sm"variant="primary">New Exam</Button></Col>
       
     </Row>
     <Row style={{width:'17%'}}>
        
        <Col ><Button id="BtnExist" style={{display:'none'}} href={href5} size="sm"variant="primary">From Existing Exams</Button></Col>
    </Row>


 </Container>
            
          </div>
        );
    }
}

export default InstructorHome;
