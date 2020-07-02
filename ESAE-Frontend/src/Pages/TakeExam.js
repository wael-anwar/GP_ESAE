import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Exam.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import TakeMCQ from './TakeMCQ.js';
import TakeEssay from './TakeEssay.js';
import TakeTF from './TakeTF.js';
import TakeComplete from './TakeComplete.js';



class TakeExam extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '',Submit:null};
        window.ExamTitle=[];
        window.ExamMCQCounter=[];
        window.ExamMCQQuestions=[];
        window.ExamMCQChoices=[];
        window.ExamComplete=[];
        window.ExamTF=[];
        window.ExamEssay=[];
        window.ExamComparsion=[];

        this.handleChange = this.handleChange.bind(this);
  
        this.handleSubmit = this.handleSubmit.bind(this);
      }


      SubmitStudentExam(StudentID, MCQList, MCQAnswers, 
        CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers)
      {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const examname = params.get('name');
        // console.log("Question",question)
        fetch('/SubmitStudentExam/'+examname+'/'+StudentID+'/'+MCQList+'/'+MCQAnswers+'/'+CompleteList+'/'+CompleteAnswers+'/'+TFList+
        '/'+TFAnswers+'/'+EssayList+'/'+EssayAnswers)
          .then(response => response.json())
          .then(data => this.setState({Submit : data.successful}));
      }

    render() {
        
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');
        return (
            <div>
    
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
        <Form.Label style={{ display: 'flex', justifyContent: 'center' }}><b>{name}</b> </Form.Label>
            <TakeMCQ passedname={name}/>
            <TakeTF passedname={name}/>
            <TakeComplete passedname={name}/>
            <TakeEssay passedname={name}/>
            <Button style={{ float:'right'}} variant="primary" type="submit">Submit Answers</Button>
        </Form>
        </Container>
            </div>
            );
    }
}

export default TakeExam;
