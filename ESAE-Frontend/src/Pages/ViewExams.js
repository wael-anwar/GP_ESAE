import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './ViewExams.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'
class ViewExams extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '',ExamList:null};//,answer:null
    }

    async GetExamTitles(){
        // console.log("Question",question)
        fetch('/ViewExams')
          .then(response => response.json())
          .then(data => this.setState({ExamList:data.ans}));
          
      }

    render() {
       var names= window.ExamTitle;
       //this.GetExamTitles()
       //var names=this.state.ExamList
       if (names==null)
       {
        var nameslist='No Exams Yet'
       }
       else
       {
        var nameslist= names.map(function(name){
            return <ListGroup.Item href="/#/instructor-exam"action>{name}</ListGroup.Item>;
          })
       }
    
        
       return (
        <div>
          
          <h1>All Exams</h1>
   
    <Container style={{width:'660px',height:'550px',backgroundColor:'white'}}>
        <br />
       <ListGroup style={{textAlign: 'center'}} >{nameslist}</ListGroup>
    </Container>
        </div>
        );
    }
}

export default ViewExams;
