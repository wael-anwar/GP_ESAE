import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './CreateExam.css';
import './Popup.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
import DropdownButton from 'react-bootstrap/DropdownButton';
import Dropdown from 'react-bootstrap/Dropdown';

class EditEssay extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', Question:null, CorrectAnswer:null, ILO:null,  Grade:null, IsUpdated:null,
        OldQuestion:null, ExamTitle:'Marketing', InstructorID:1};
        this.GetEssayInfo()
        //this.Autofill()
        
          
    }

    //this is for one question
    GetEssayInfo()
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
        fetch('/GetAEssQues/'+exam+'/'+1+'/'+question)
            .then(response => response.json())
            .then(data => this.setState({Question:data.Question, CorrectAnswer:data.CorrectAnswer, ILO:data.ILO,  Grade:data.Grade}));
    }

    UpdateEssay(NewQuestion, NewCorrectAns, NewILO, NewGrade)
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
      fetch('/UpdateEssay/'+question+'/'+NewQuestion+'/'+NewCorrectAns+'/'+exam+'/'
      +NewILO+'/'+NewGrade+'/'+1)
        .then(response => response.json())
        .then(data => this.setState({IsUpdated:data.Updated}));
    }

    // async Autofill()
    // {
    //     document.getElementById('EssayILO').value=this.state.ILO;
    //     document.getElementById('EssayGrade').value=this.state.Grade;
    //     document.getElementById('TextEssay').value=this.state.Question;
    //     document.getElementById('AnswerEssay').value=this.state.CorrectAnswer;
    // }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
    render() {
        return (
        <div>
<Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
        <br />
<Form.Group  id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="EssayILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state['ILO']} 
    placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm" id="EssayGrade"style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" value={this.state['Grade']}
    placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextEssay" type="text" value={this.state['Question']} placeholder="Enter Your Essay Question" />
   <br />
    <Form.Control size="sm" as="textarea"id="AnswerEssay" value={this.state['CorrectAnswer']} placeholder="Enter Your Model Answer" />
    <Button size="sm" style={{ float:'right'}} variant="success"
     onClick={()=>{this.UpdateEssay(document.getElementById('TextEssay').value, 
     document.getElementById('AnswerEssay').value, document.getElementById('EssayILO').value, 
     document.getElementById('EssayGrade').value)
     }}
      >Save Changes</Button>
    </Form.Group>
    </Container>
        </div>
        )
    }
}
export default EditEssay;