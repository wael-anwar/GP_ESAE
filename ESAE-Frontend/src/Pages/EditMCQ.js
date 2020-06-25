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

class EditMCQ extends Component {
    Autofill()
    {
        document.getElementById('MCQILO').value="ilo";
        document.getElementById('MCQGrade').value="grade";
        document.getElementById('TextMCQuestion').value="text";
        document.getElementById('ChoiceModelAns').value="answer";
    }
   handleSave()
   {
    //eb3t database
    alert("Saved Successfully")
   }
   handleAddChoice()
      { 
        
        var x = document.createElement("div");
        x.setAttribute("class", "form-check form-check-inline");
        x.setAttribute("id","choice"+window.ChoiceCounter);
        x.innerHTML='<input type="radio" disabled class="form-check-input">'+
        '<label title for="formExamMCQ" id= "'+"choice"+window.ChoiceCounter+'" class="form-check-label">'+ document.getElementById('formChoiceTextbox').value+'</label>';
        document.getElementById('ChoicesDiv').appendChild(x);
        window.ChoiceCounter++;
        var y=document.createElement("option");
        y.innerText=document.getElementById('formChoiceTextbox').value;
        document.getElementById('ChoiceModelAns').appendChild(y);
        document.getElementById('formChoiceTextbox').value='';
      }
      handleDeleteChoice()
      {
        window.ChoiceCounter--;
        var y=document.getElementById('choice'+window.ChoiceCounter);
        document.getElementById('ChoicesDiv').removeChild(y);
      }
    render() {
        return (
        <div>
<Form.Group  style={{display:'none'}} id="formExamMCQ" controlId="formExamMCQ">
 
 <Form.Label>Multiple Choice Question</Form.Label>
 <Row>
 <Form.Control  size="sm" type="text" id="MCQILO" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
<Form.Control required size="sm"id="MCQGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />

</Row>
 <Form.Control required size="sm" id="TextMCQuestion" type="text" placeholder="Enter Your Question" />
 <br />
 <Form.Control  required size="sm" id="formChoiceTextbox" type="text" placeholder="Enter a Choice" />
 <Button  size="sm" variant="primary" onClick={this.handleAddChoice}>Add Choice</Button>
 <Button id="btnDeleteChoice"  size="sm" variant="danger" onClick={this.handleDeleteChoice}>Delete Choice</Button>
 <div id="ChoicesDiv"></div>
 <Form.Control required size="sm" as="select" id="ChoiceModelAns" placeholder="Choose Model Answer">
 <option>Choose Model Answer</option>
 </Form.Control>
 <Button size="sm" style={{ float:'right'}} variant="success"onClick={this.handleSave} >Save Changes</Button>
</Form.Group>
        </div>
        )
    }
}
export default EditMCQ;