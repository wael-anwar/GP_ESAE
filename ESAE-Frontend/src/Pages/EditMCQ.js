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

class EditMCQ extends Component {

    constructor(props) {
      super(props);
      this.state = {value: '', Question:null, AnswerList:null, CorrectAnswer:null, ILO:null,  Grade:null, IsUpdated:null,
      OldQuestion:null};
      //this.GetMCQInfo()
      this.Autofill()
      
    }

    //this is for one question
    async GetMCQInfo()
    {
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      const exam = params.get('exam');
      //params = new URLSearchParams(window.location.hash.split("?")[2]);
      const question = params.get('question');
      const id = params.get('id');
      const response = await fetch('/GetAMCQ/'+exam+'/'+id+'/'+question).then(response => response.json());
      this.setState({Question:response.Question, AnswerList:response.AnswerList,
          CorrectAnswer:response.CorrectAnswer, ILO:response.ILO,  Grade:response.Grade});

    
    }

    async FetchUpdateMCQ(question, NewQuestion, NewAnswers, NewCorrectAns, exam, NewILO, NewGrade, id)
    {
        const response = await fetch('/UpdateMCQ/'+question+'/'+NewQuestion+'/'+NewAnswers+'/'+NewCorrectAns+'/'+exam+'/'
        +NewILO+'/'+NewGrade+'/'+id).then(response => response.json());
        this.setState({IsUpdated:response.Updated});
    }

    //et2aked ml choices variable
    async UpdateMCQ(NewQuestion, NewAnswers, NewCorrectAns, NewILO, NewGrade)
    {
      window.ExamMCQChoices=[]
      
      for(var i=0;i<window.ChoiceCounter;i++)
      {
        
        window.ExamMCQChoices.push(document.getElementById('choice'+i).textContent)
      }
      NewAnswers=window.ExamMCQChoices;
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      const exam = params.get('exam');
      //params = new URLSearchParams(window.location.hash.split("?")[2]);
      const question = params.get('question');
      const id = params.get('id');
      await this.FetchUpdateMCQ(question, NewQuestion, NewAnswers, NewCorrectAns, exam, NewILO, NewGrade, id)
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
        await this.GetMCQInfo();
        document.getElementById('MCQILO').value=this.state.ILO;
        document.getElementById('MCQGrade').value=this.state.Grade;
        document.getElementById('TextMCQuestion').value=this.state.Question;
       
        var ExamMCQChoices=this.state.AnswerList;
      
        ExamMCQChoices = ExamMCQChoices.toString().split(',');
        window.ChoiceCounter=0;
        for(var i=0;i<ExamMCQChoices.length;i++)
        {
          var x = document.createElement("div");
          x.setAttribute("class", "form-check form-check-inline");
          x.setAttribute("id","choice"+i);
          x.innerHTML='<input type="radio" disabled class="form-check-input">'+
          '<label title for="formExamMCQ" id= "'+"choice"+i+'" class="form-check-label">'+ ExamMCQChoices[i]+'</label>';
          document.getElementById('ChoicesDiv').appendChild(x);
          
          var y=document.createElement("option");
          y.innerText=ExamMCQChoices[i];
          y.setAttribute("id","option"+i);
          document.getElementById('ChoiceModelAns').appendChild(y);
          window.ChoiceCounter=i;
        }
        window.ChoiceCounter+=1;
        document.getElementById('ChoiceModelAns').value=this.state.CorrectAnswer;
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

   handleAddChoice()
   { 
     
     var x = document.createElement("div");
     x.setAttribute("class", "form-check form-check-inline");
     x.setAttribute("id","choice"+window.ChoiceCounter);
     x.innerHTML='<input type="radio" disabled class="form-check-input">'+
     '<label title for="formExamMCQ" id= "'+"choice"+window.ChoiceCounter+'" class="form-check-label">'+ document.getElementById('formChoiceTextbox').value+'</label>';
     document.getElementById('ChoicesDiv').appendChild(x);
     
     var y=document.createElement("option");
     y.innerText=document.getElementById('formChoiceTextbox').value;
     y.setAttribute("id","option"+window.ChoiceCounter);
     document.getElementById('ChoiceModelAns').appendChild(y);
     document.getElementById('formChoiceTextbox').value='';
     window.ChoiceCounter++;
   }
   handleDeleteChoice()
   {
     window.ChoiceCounter--;
     var y=document.getElementById('choice'+window.ChoiceCounter);
     var z=document.getElementById('option'+window.ChoiceCounter);
     document.getElementById('ChoicesDiv').removeChild(y);
     document.getElementById('ChoiceModelAns').removeChild(z);
   }
    render() {
        return (
        <div>
      <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
              <br />
      <Form.Group   id="formExamMCQ" controlId="formExamMCQ">
      
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
      <Button size="sm" style={{ float:'right'}} variant="success"
      onClick={()=>{this.UpdateMCQ(document.getElementById('TextMCQuestion').value, 
      window.ExamMCQChoices, document.getElementById('ChoiceModelAns').value, 
      document.getElementById('MCQILO').value, document.getElementById('MCQGrade').value)
      }}
        >Save Changes</Button>
      </Form.Group>
      </Container>

>>>>>>> Yousry_Evaluate
        </div>
        )
    }
}
export default EditMCQ;