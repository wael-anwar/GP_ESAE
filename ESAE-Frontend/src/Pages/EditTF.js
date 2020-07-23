import React, { Component } from 'react';
<<<<<<< HEAD
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
=======
//import { Link } from 'react-router-dom';
import './CreateExam.css';
import './Popup.css';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
//import DropdownButton from 'react-bootstrap/DropdownButton';
//import Dropdown from 'react-bootstrap/Dropdown';

class EditTF extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', Question:null, CorrectAnswer:null, ILO:null,  Grade:null, IsUpdated:null,
        OldQuestion:null};
        //this.GetTFInfo()
        this.Autofill()
          
    }

    //this is for one question
    async GetTFInfo()
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
        const id = params.get('id');
        const response = await fetch('/GetATrueFalseQues/'+exam+'/'+id+'/'+question).then(response => response.json());
        this.setState({Question:response.Question, CorrectAnswer:response.CorrectAnswer, ILO:response.ILO,  Grade:response.Grade});

    }

    async FetchUpdateTF(question, NewQuestion, NewCorrectAns, exam, NewILO, NewGrade, id)
    {
        const response = await fetch('/UpdateTrueFalse/'+question+'/'+NewQuestion+'/'+NewCorrectAns+'/'+exam+'/'
        +NewILO+'/'+NewGrade+'/'+id).then(response => response.json());
        this.setState({IsUpdated:response.Updated});
    }

    async UpdateTrueFalse(NewQuestion, NewCorrectAns, NewILO, NewGrade)
    {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const exam = params.get('exam');
        //params = new URLSearchParams(window.location.hash.split("?")[2]);
        const question = params.get('question');
        const id = params.get('id');

        await this.FetchUpdateTF(question, NewQuestion, NewCorrectAns, exam, NewILO, NewGrade, id)
        if (this.state.IsUpdated == "Successfully updated")
        {
            alert("Successfully updated")
        }
        else
        {
            alert("There was an issue in update, please try again")
        }
        
        //this.handleSave();
    }

    async Autofill()
    {
        await this.GetTFInfo();
        document.getElementById('TFILO').value=this.state.ILO;
        document.getElementById('TFGrade').value=this.state.Grade;
        document.getElementById('TextTF').value=this.state.Question;
        document.getElementById('TFModelAns').value=this.state.CorrectAnswer;
    }

    handleSave()
    {
     if (this.state.IsUpdated == "Successfully updated")
     {
       alert("Saved Successfully");
     }
     else
     {
       alert("Unsuccessful try");
       window.location.reload(false);
     } 
    }

    render() {
        return (
        <div>
<Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
        <br />
<Form.Group  id="formExamTF" controlId="formExamTF">
    <Form.Label>True and False Question</Form.Label>
    <Row>
    <Form.Control  size="sm"id="TFILO" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}}
    placeholder="Enter Question ILO"></Form.Control>
   <Form.Control size="sm"id="TFGrade" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number"
   placeholder="Enter Your Grade" />
>>>>>>> Yousry_Evaluate
   
   </Row>
    <Form.Control size="sm" id="TextTF" type="text" placeholder="Enter Your Question" />
      <br />
      <Form.Control size="sm" as="select" id="TFModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    <option>True</option>
    <option>False</option>
    </Form.Control>
<<<<<<< HEAD
    <Button size="sm" style={{ float:'right'}} variant="success"onClick={this.handleSave} >Save Changes</Button>
   
    </Form.Group>
=======
    <Button size="sm" style={{ float:'right'}} variant="success"
    onClick={()=>{this.UpdateTrueFalse(document.getElementById('TextTF').value, 
    document.getElementById('TFModelAns').value, document.getElementById('TFILO').value, 
    document.getElementById('TFGrade').value)
    }}
     >Save Changes</Button>
   
    </Form.Group>
    </Container>
    
>>>>>>> Yousry_Evaluate
        </div>
        )
    }
}
export default EditTF;