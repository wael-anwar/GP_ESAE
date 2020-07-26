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
import Spinner from 'react-bootstrap/Spinner'
import Row from 'react-bootstrap/Row';

class TakeExam extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '',Submit:null, id:null, username:null};

      }

      handleSubmitAnswers()
      {
        document.getElementById("Progressbar").style.display='none';
        document.getElementById('ExamSubmitBox').style.display='block';
      }

      async FetchSubmitExam(examname, id, MCQList, MCQAnswers, CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers)
      {
        const response = await fetch('/SubmitStudentExam/'+examname+'/'+id+'/'+MCQList+'/'+MCQAnswers+'/'+CompleteList+'/'
        +CompleteAnswers+'/'+TFList+'/'+TFAnswers+'/'+EssayList+'/'+EssayAnswers).then(response => response.json());
        this.setState({Submit:response.successful});
      }

      async GetNamyByID()
      {
        const response = await fetch('/GetStudNamebyID/'+this.state.id).then(response => response.json());
        this.setState({username:response.name});
      }
      showProgress()
      {
        document.getElementById("Progressbar").style.display='block';
      }
      async SubmitStudentExam(MCQList, MCQAnswers, 
        CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers)
      {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const examname = params.get('name');
        const id = params.get('id');
        this.state.id=id;
        this.showProgress();
        // console.log("Question",question)
        if (MCQList.length==0 || MCQList==null||MCQList[0]=="")
        {
          //alert("d5l fel mcq Q")
          MCQList = ['empty']
        }
        if (MCQAnswers.length==0 || MCQAnswers==null||MCQAnswers[0]=="")
        {
          //alert("d5l fel mcq answer")
          MCQAnswers = ['empty']
        }
        if (CompleteList.length==0 || CompleteList==null||CompleteList[0]=="")
        {
         // alert("d5l fel Comp Q")
          CompleteList = ['empty']
        }
        if (CompleteAnswers.length==0 || CompleteAnswers==null||CompleteAnswers[0]=="")
        {
          //alert("d5l fel comp answer")
          CompleteAnswers = ['empty']
        }
        if (TFList.length==0 || TFList==null||TFList[0]=="")
        {
         // alert("d5l fel TF Q")
          TFList = ['empty']
        }
        if (TFAnswers.length==0 || TFAnswers==null||TFAnswers[0]=="")
        {
          //alert("d5l fel tf answer")
          TFAnswers = ['empty']
        }
        if (EssayList.length==0 || EssayList==null||EssayList[0]=="")
        {
          //alert("d5l fel Ess Q")
          EssayList = ['empty']
        }
        if (EssayAnswers.length==0 || EssayAnswers==null||EssayAnswers[0]=="")
        {
          //alert("d5l fel ess answer")
          EssayAnswers = ['empty']
        }
        
        //alert(id)
        //alert(MCQList)
        await this.FetchSubmitExam(examname, id, MCQList, MCQAnswers, CompleteList, CompleteAnswers, TFList, TFAnswers, EssayList, EssayAnswers)
        await this.GetNamyByID()
        if (this.state.Submit == 'Exam is submitted')
        {
          this.handleSubmitAnswers();
        }
        else
        {
          alert('There was an issue in submitting the exam, please try again.')
        }
        
        //alert(MCQList)
      }

    render() {
        
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');
        const username=this.state.username;
        var home = `#/student-home?${new URLSearchParams({username}).toString()}`;
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
              <Button variant="primary" onClick={event =>  window.location.href=home} >Ok</Button>
            </Modal.Footer>
          </Modal.Dialog>
          </div>
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
        <Form.Label style={{ color:'red',display: 'flex', justifyContent: 'center', fontStyle: 'italic', fontWeight: 'bold', textDecorationLine: 'underline' }}><b>{name}</b> </Form.Label>
            <TakeMCQ passedname={name}/>
            <br></br>
            <TakeTF passedname={name}/>
            <br></br>
            <TakeComplete passedname={name}/>
            <br></br>
            <TakeEssay passedname={name}/>
            <Button style={{ float:'right'}} variant="primary"  onClick={()=>{this.SubmitStudentExam(window.MCQQuestions,window.MCQAnswers,window.CompleteQuestions,window.CompleteAnswers,window.TFQuestions,window.TFAnswers,window.EssayQuestions,window.EssayAnswers)}}>Submit Answers</Button>
            <Row style={{justifyContent:'center'}}>
      <Spinner style={{display:'none'}} id="Progressbar" animation="border" variant="primary" role="status">
       <span className="sr-only">Loading...</span>
        </Spinner>
      </Row>
        </Form>
        </Container>
            </div>
            );
    }
}

export default TakeExam;
