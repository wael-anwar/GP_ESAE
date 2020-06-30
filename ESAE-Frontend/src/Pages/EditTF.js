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

class EditTF extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', Question:null, CorrectAnswer:null, ILO:null,  Grade:null, IsUpdated:null,
        OldQuestion:null, ExamTitle:'Marketing', InstructorID:1};
        this.GetTFInfo()
        //this.Autofill()
          
    }

    //this is for one question
    GetTFInfo()
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
        fetch('/GetATrueFalseQues/'+exam+'/'+1+'/'+question)
            .then(response => response.json())
            .then(data => this.setState({Question:data.Question, CorrectAnswer:data.CorrectAnswer, ILO:data.ILO,  Grade:data.Grade}));
    }

    UpdateTrueFalse(NewQuestion, NewCorrectAns, NewILO, NewGrade)
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
      fetch('/UpdateTrueFalse/'+question+'/'+NewQuestion+'/'+NewCorrectAns+'/'+exam+'/'
      +NewILO+'/'+NewGrade+'/'+1)
        .then(response => response.json())
        .then(data => this.setState({IsUpdated:data.Updated}));
    }

    // Autofill()
    // {
    //     document.getElementById('TFILO').value=this.state.ILO;
    //     document.getElementById('TFGrade').value=this.state.Grade;
    //     document.getElementById('TextTF').value=this.state.Question;
    //     document.getElementById('TFModelAns').value=this.state.CorrectAnswer;
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
<Form.Group  id="formExamTF" controlId="formExamTF">
    <Form.Label>True and False Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="TFILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state['ILO']} 
    placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm"id="TFGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" value={this.state['Grade']} 
   placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextTF" type="text" value={this.state['Question']} placeholder="Enter Your Question" />
      <br />
      <Form.Control size="sm" as="select" id="TFModelAns" value={this.state['CorrectAnswer']}  placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    <option>True</option>
    <option>False</option>
    </Form.Control>
    <Button size="sm" style={{ float:'right'}} variant="success"
    onClick={()=>{this.UpdateTrueFalse(document.getElementById('TextTF').value, 
    document.getElementById('TFModelAns').value, document.getElementById('TFILO').value, 
    document.getElementById('TFGrade').value)
    }}
     >Save Changes</Button>
   
    </Form.Group>
    </Container>
    
        </div>
        )
    }
}
export default EditTF;