import React, { Component } from 'react';

import './Exam.css';

import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';

import TakeMCQ from './TakeMCQ.js';
import TakeEssay from './TakeEssay.js';
import TakeTF from './TakeTF.js';
import TakeComplete from './TakeComplete.js';
import Modal from 'react-bootstrap/Modal'


class TakeExam extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '',Submit:null};

      }

      handleSubmitAnswers()
      {
        document.getElementById('ExamSubmitBox').style.display='block';
      }
      SubmitStudentExam(StudentID, MCQList, MCQAnswers, 
        CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers)
      {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const examname = params.get('name');
        // console.log("Question",question)
        if (MCQList==[])
        {
          MCQList = ['']
        }
        if (MCQAnswers==[])
        {
          MCQAnswers = ['']
        }
        if (CompleteList==[])
        {
          CompleteList = ['']
        }
        if (CompleteAnswers==[])
        {
          CompleteAnswers = ['']
        }
        if (TFList==[])
        {
          TFList = ['']
        }
        if (TFAnswers==[])
        {
          TFAnswers = ['']
        }
        if (EssayList==[])
        {
          EssayList = ['']
        }
        if (EssayAnswers==[])
        {
          EssayAnswers = ['']
        }
        fetch('/SubmitStudentExam/'+examname+'/'+StudentID+'/'+MCQList+'/'+MCQAnswers+'/'+CompleteList+'/'+CompleteAnswers+'/'+TFList+
        '/'+TFAnswers+'/'+EssayList+'/'+EssayAnswers)
          .then(response => response.json())
          .then(data => this.setState({Submit : data.successful}));
          this.handleSubmitAnswers();
      }

    render() {
        
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');
        return (
            <div>
     <div style={{display:'none'}} class="modal-custom" id="ExamSubmitBox">
          <Modal.Dialog  >
              <Modal.Header >
              <Modal.Title>Exam Alert</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                Exam "{name}" Submitted Successfully
            </Modal.Body>
            <Modal.Footer>
              <Button variant="primary" onClick={event =>  window.location.href='#/student-home'} >Ok</Button>
            </Modal.Footer>
          </Modal.Dialog>
          </div>
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
        <Form.Label style={{ display: 'flex', justifyContent: 'center' }}><b>{name}</b> </Form.Label>
            <TakeMCQ passedname={name}/>
            <TakeTF passedname={name}/>
            <TakeComplete passedname={name}/>
            <TakeEssay passedname={name}/>
            <Button style={{ float:'right'}} variant="primary"  type="submit"onClick={()=>{this.SubmitStudentExam('1',window.MCQQuestions,window.MCQAnswers,window.CompleteQuestions,window.CompleteAnswers,window.TFQuestions,window.TFAnswers,window.EssayQuestions,window.EssayAnswers)}}>Submit Answers</Button>
        </Form>
        </Container>
            </div>
            );
    }
}

export default TakeExam;
