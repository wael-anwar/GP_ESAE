import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './StudentHome.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
class StudentHome extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', fullname:null, id:null};
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const username=params.get('username')
        this.GetName(username)
  
    }

    GetName(username)
    {
      fetch('/GetStudName/'+username)
        .then(response => response.json())
        .then(data => this.setState({fullname : data.name, id:data.id}));
    }

    render() {
        window.StudentName = this.state.fullname
        const id = this.state.id
        const href1 = `#/student-view-all?${new URLSearchParams({id}).toString()}`;
        return (
        <div>
          
          <h1>Welcome {window.StudentName}</h1>
    <br />
    <Container style={{ justifyContent:'center'}}>
     <Row style={{ justifyContent:'space-evenly'}}>
         <Col  style={{ flexGrow:'unset'}}><Button style={{width: 'max-content'}} href="#/student-ask" size="lg"variant="primary">Ask a Question</Button></Col>
         <Col style={{ flexGrow:'unset'}} ><Button style={{width: 'max-content'}} href={href1} size="lg" variant="primary">Take Exam</Button></Col>
     </Row>

 </Container>
            
          </div>
        );
    }
}

export default StudentHome;
