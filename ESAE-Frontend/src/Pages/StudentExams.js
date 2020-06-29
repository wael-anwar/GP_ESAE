import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './StudentExams.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'
class StudentExams extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', Exams:null};
        fetch('/ViewExams/'+1)
          .then(response => response.json())
          .then(data => this.setState({Exams : data.ans}));
          
    }

    render() {
       //var names= window.ExamTitle;
       var names = this.state.Exams
       if (names==null)
       {
        var nameslist='No Exams Yet'
       }
       else
       {
        var nameslist= names.map(function(name){
            return  <ListGroup.Item action>{name}</ListGroup.Item>;
          })
       }
    
        
       return (
        <div>
          
          <h1>All Exams</h1>
   
    <Container style={{width:'660px',height:'550px',backgroundColor:'white',overflow:'scroll'}}>
        <br />
       <ListGroup style={{textAlign: 'center'}} >{nameslist}</ListGroup>
    </Container>
        </div>
        );
    }
}

export default StudentExams;
