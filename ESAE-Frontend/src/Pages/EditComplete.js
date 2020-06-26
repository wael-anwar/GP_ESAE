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
    Autofill()
    {
        document.getElementById('CompleteILO').value="ilo";
        document.getElementById('CompleteGrade').value="grade";
        document.getElementById('TextComplete1').value="text1";
        document.getElementById('TextComplete2').value="text2";
        document.getElementById('AnswerComplete').value="answer";
    }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
    render() {
        return (
        <div>
<Form.Group style={{display:'none'}} id="formExamComplete" controlId="formExamComplete">
   
   <Form.Label>Complete Question</Form.Label>
   <Row>
   <Form.Control  size="sm" id="CompleteILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm" id="CompleteGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
   <Form.Control size="sm" id="TextComplete1" type="text" placeholder="Enter Your 1st part of the Question *before the space*" />
   <Form.Control size="sm"id="TextComplete2" type="text" placeholder="Enter Your 2nd part of the Question *after the space*" />
   <br />
   <Form.Control size="sm" id="AnswerComplete" type="text" placeholder="Enter Your Model Answer *the space*" />
   <Button size="sm" style={{ float:'right'}} variant="success"onClick={this.handleSave} >Save Changes</Button>
   
   </Form.Group>
        </div>
        )
    }
}
export default EditComplete;