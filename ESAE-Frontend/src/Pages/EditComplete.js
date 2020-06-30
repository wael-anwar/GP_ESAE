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

class EditComplete extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', Question1:null, Question2:null, CorrectAnswer:null, ILO:null,  Grade:null, IsUpdated:null, 
        InstructorID:1, ExamTitle:'Marketing', OldQuestion1:null, OldQuestion2:null};
        this.GetCompleteInfo()
        //this.Autofill()
        
          
    }

    //this is for one question
    GetCompleteInfo()
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
        fetch('/GetACompleteQues/'+exam+'/'+1+'/'+question)
            .then(response => response.json())
            .then(data => this.setState({Question1:data.Question1, Question2:data.Question2, 
            CorrectAnswer:data.CorrectAnswer, ILO:data.ILO,  Grade:data.Grade}));
    }

    UpdateComplete(NewQuestion1, NewQuestion2, NewCorrectAns, NewILO, NewGrade)
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
      fetch('/UpdateComplete/'+question+'/'+NewQuestion1+'/'+NewQuestion2+'/'
      +NewCorrectAns+'/'+exam+'/'+NewILO+'/'+NewGrade+'/'+1)
        .then(response => response.json())
        .then(data => this.setState({IsUpdated:data.Updated}));

    }

    // Autofill()
    // {
    //     document.getElementById('CompleteILO').value=this.state.ILO;
    //     document.getElementById('CompleteGrade').value=this.state.Grade;
    //     document.getElementById('TextComplete1').value=this.state.Question1;
    //     document.getElementById('TextComplete2').value=this.state.Question2;
    //     document.getElementById('AnswerComplete').value=this.state.CorrectAnswer;
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
<Form.Group id="formExamComplete" controlId="formExamComplete">
   
   <Form.Label>Complete Question</Form.Label>
   <Row>
   <Form.Control  size="sm" id="CompleteILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state['ILO']} 
   placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm" id="CompleteGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" value={this.state['Grade']} 
   placeholder="Enter Your Grade" />
   
   </Row>
   <Form.Control size="sm" id="TextComplete1" type="text" value={this.state['Question1']}  placeholder="Enter Your 1st part of the Question *before the space*" />
   <Form.Control size="sm"id="TextComplete2" type="text" value={this.state['Question2']}  placeholder="Enter Your 2nd part of the Question *after the space*" />
   <br />
   <Form.Control size="sm" id="AnswerComplete" type="text" value={this.state['CorrectAnswer']} placeholder="Enter Your Model Answer *the space*" />
   <Button size="sm" style={{ float:'right'}} variant="success"
   onClick={()=>{this.UpdateComplete(document.getElementById('TextComplete1').value, 
   document.getElementById('TextComplete2').value, document.getElementById('AnswerComplete').value,
    document.getElementById('CompleteILO').value, document.getElementById('CompleteGrade').value)
   }}
   >Save Changes</Button>
   
   </Form.Group>
   </Container>
        </div>
        )
    }
}
export default EditComplete;