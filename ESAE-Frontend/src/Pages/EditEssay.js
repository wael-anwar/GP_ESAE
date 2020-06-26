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
    Autofill()
    {
        document.getElementById('EssayILO').value="ilo";
        document.getElementById('EssayGrade').value="grade";
        document.getElementById('TextEssay').value="text";
        document.getElementById('AnswerEssay').value="answer";
    }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
    render() {
        return (
        <div>
<Form.Group style={{display:'none'}} id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="EssayILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm" id="EssayGrade"style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextEssay" type="text" placeholder="Enter Your Essay Question" />
   <br />
    <Form.Control size="sm" as="textarea"id="AnswerEssay" placeholder="Enter Your Model Answer" />
    <Button size="sm" style={{ float:'right'}} variant="success"onClick={this.handleSave} >Save Changes</Button>
    </Form.Group>
        </div>
        )
    }
}
export default EditEssay;