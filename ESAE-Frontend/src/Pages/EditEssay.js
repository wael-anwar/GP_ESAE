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
        this.Autofill()
        
          
    }

    //this is for one question
    GetEssayInfo(ExamTitle,InstructorID,Question)
    {
        fetch('/GetAEssQues/'+ExamTitle+'/'+InstructorID+'/'+Question)
            .then(response => response.json())
            .then(data => this.setState({Question:data.Question, CorrectAnswer:data.CorrectAnswer, ILO:data.ILO,  Grade:data.Grade}));
    }

    UpdateEssay(NewQuestion, NewCorrectAns, NewILO, NewGrade)
    {
      fetch('/UpdateEssay/'+this.state.OldQuestion+'/'+NewQuestion+'/'+NewCorrectAns+'/'+this.state.ExamTitle+'/'
      +NewILO+'/'+NewGrade+'/'+this.state.InstructorID)
        .then(response => response.json())
        .then(data => this.setState({IsUpdated:data.Updated}));
    }

    Autofill()
    {
        document.getElementById('EssayILO').value=this.state.ILO;
        document.getElementById('EssayGrade').value=this.state.Grade;
        document.getElementById('TextEssay').value=this.state.Question;
        document.getElementById('AnswerEssay').value=this.state.CorrectAnswer;
    }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
    render() {
        return (
        <div>
<Form.Group  id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="EssayILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm" id="EssayGrade"style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextEssay" type="text" placeholder="Enter Your Essay Question" />
   <br />
    <Form.Control size="sm" as="textarea"id="AnswerEssay" placeholder="Enter Your Model Answer" />
    <Button size="sm" style={{ float:'right'}} variant="success"
    onClick={()=>{this.UpdateEssay(document.getElementById('TextEssay').value, 
    document.getElementById('AnswerEssay').value, document.getElementById('EssayILO').value, 
    document.getElementById('EssayGrade').value)
    }}
    >Save Changes</Button>
    </Form.Group>
        </div>
        )
    }
}
export default EditEssay;