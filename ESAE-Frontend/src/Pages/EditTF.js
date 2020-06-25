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
    Autofill()
    {
        document.getElementById('TFILO').value="ilo";
        document.getElementById('TFGrade').value="grade";
        document.getElementById('TextTF').value="text";
        document.getElementById('TFModelAns').value="answer";
    }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
    render() {
        return (
        <div>
<Form.Group style={{display:'none'}} id="formExamTF" controlId="formExamTF">
    <Form.Label>True and False Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="TFILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm"id="TFGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextTF" type="text" placeholder="Enter Your Question" />
      <br />
      <Form.Control size="sm" as="select" id="TFModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    <option>True</option>
    <option>False</option>
    </Form.Control>
    <Button size="sm" style={{ float:'right'}} variant="success"onClick={this.handleSave} >Save Changes</Button>
   
    </Form.Group>
        </div>
        )
    }
}
export default EditTF;