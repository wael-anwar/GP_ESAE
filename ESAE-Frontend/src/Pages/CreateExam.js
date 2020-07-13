import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import ReactDOM from 'react-dom';
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
import Modal from 'react-bootstrap/Modal'
import $ from 'jquery'; 
import Alert from 'react-bootstrap/Alert'
import Overlay from 'react-bootstrap/Overlay'
import Popover from 'react-bootstrap/Popover'
import OverlayTrigger from 'react-bootstrap/OverlayTrigger'

class CreateExam extends Component {
  
    constructor(props) {
        super(props);
        this.state = {value: '',answer:null, MCQreturn:null,Completereturn:null, TFreturn:null, Essayreturn:null,finished:false, id:null};
        window.ExamTitleBOX=[];
        window.ExamMCQCounter=[];
        window.ExamMCQQuestions=[];
        window.ExamMCQChoices=[];
        window.ExamComplete=[];
        window.ExamTF=[];
        window.ExamEssay=[];
        //alert(window.IDToken)
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const ID = params.get('IDToken');
        this.state.id=ID
        

        this.handleChange = this.handleChange.bind(this);
  
        this.handleSubmit = this.handleSubmit.bind(this);
      }
      handleChange (event) {
        this.setState({value: event.target.value});
      }
      SubmitMCQ(ExamTitle,Question,Answers,CorrectAns,Grade,ILO)
      {
        this.handleFinishQuestion()
        // console.log("Question",question)
        fetch('/AddMCQ/'+ExamTitle+'/'+this.state.id+'/'+Question+'/'+Answers+'/'+CorrectAns+'/'+Grade+'/'+ILO)
          .then(response => response.json())
          .then(data => this.setState({MCQreturn : data.MCQReturn}));
      }
     
      SubmitComplete(ExamTitle,Question1,Question2,Answer,Grade,ILO)
      {
        this.handleFinishQuestion()
        // console.log("Question",question)
        fetch('/AddComplete/'+ExamTitle+'/'+this.state.id+'/'+Question1+'/'+Question2+'/'+Answer+'/'+Grade+'/'+ILO)
          .then(response => response.json())
          .then(data => this.setState({Completereturn : data.CompleteReturn}));
      }

      SubmitTrueFalse(ExamTitle, Question,Answer,Grade,ILO)
      {
        //alert(window.IDToken)
        this.handleFinishQuestion()
        // console.log("Question",question)
        fetch('/AddTrueFalse/'+ExamTitle+'/'+this.state.id+'/'+Question+'/'+Answer+'/'+Grade+'/'+ILO)
          .then(response => response.json())
          .then(data => this.setState({TFreturn : data.TFReturn}));
      }

      SubmitEssay(ExamTitle, Question,Answer,Grade,ILO)
      {
        this.handleFinishQuestion()
        // console.log("Question",question)
        fetch('/AddEssay/'+ExamTitle+'/'+this.state.id+'/'+Question+'/'+Answer+'/'+Grade+'/'+ILO)
          .then(response => response.json())
          .then(data => this.setState({Essayreturn : data.EssayReturn}));
      }

      handleSubmit(event)
      {
        this.setState({finished: false});
        if (this.state.value=='MCQ')
        {
            document.getElementById('formExamMCQ').style.display='block';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
           
            window.ChoiceCounter=0;
            
        }
      else  if (this.state.value=='Complete')
        {
            document.getElementById('formExamComplete').style.display='block';
            document.getElementById('formExamMCQ').style.display='none';
            document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
         
        }
       else if (this.state.value=='T and F')
        {
          document.getElementById('formExamTF').style.display='block';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamMCQ').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
           
        }
       else if (this.state.value=='Essay Question')
        {
          document.getElementById('formExamEssay').style.display='block';
          document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamMCQ').style.display='none';
          
        }
        else
        {
          document.getElementById('formExamMCQ').style.display='none';
          document.getElementById('formExamComplete').style.display='none';
          document.getElementById('formExamTF').style.display='none';
          document.getElementById('formExamEssay').style.display='none';
        
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

      handleFinishQuestion()
      {
        if (document.getElementById('QuestionType').value=='MCQ')
        {
          window.ExamMCQQuestions.push(document.getElementById('TextMCQuestion').value);
          window.ExamMCQCounter.push(window.ChoiceCounter);
          for(var i=0;i<window.ChoiceCounter;i++)
          {
            
            window.ExamMCQChoices.push(document.getElementById('choice'+i).textContent)
          }


        }
        if (document.getElementById('QuestionType').value=='Complete')
        {
          

          window.ExamComplete.push(document.getElementById('TextComplete1').value)
          window.ExamComplete.push(document.getElementById('TextComplete2').value)
      
        }
        if (document.getElementById('QuestionType').value=='T and F')
        {
          window.ExamTF.push(document.getElementById('TextTF').value)
        }
        if (document.getElementById('QuestionType').value=='Essay Question')
        {
          window.ExamEssay.push(document.getElementById('TextEssay').value)
        }
        document.getElementById("ExamForm").reset();
        $("#ChoiceModelAns").empty();
        $("#ChoicesDiv").empty();
        var y=document.createElement("option");
        y.innerText="Choose Model Answer"
        document.getElementById('ChoiceModelAns').appendChild(y);
        document.getElementById('formExamMCQ').style.display='none';
          document.getElementById('formExamComplete').style.display='none';
          document.getElementById('formExamTF').style.display='none';
          document.getElementById('formExamEssay').style.display='none';
    
          this.setState({finished: true});
         
      }
     
      handleFinishExam()
      {
        
        window.ExamTitle.push(document.getElementById('TextExamTitle').value);
        document.getElementById('ExamFinishBox').style.display='block';
        
      }
      handleConfirm()
      {
          
          if (document.getElementById('TextExamTitle').value=="")
          {
              alert("You Must Enter an Exam Title First !")
          }
          else
          {
              window.ExamTitleBOX=document.getElementById('TextExamTitle').value
              document.getElementById('ExamtitleBox').style.display='none';
          }
          
      }
      hideAlert(){
        document.getElementById("FinishQuestionAlert").style.display="none";
      }
    render() {
      var FinishQuestionAlert = "";
      if (this.state.finished==true)
      {
        FinishQuestionAlert = <div id="FinishQuestionAlert"> <Alert  key="FinishQuestionAlert" variant='success'>Successfully Added Question to Exam<div className="d-flex justify-content-end">
        <Button onClick={this.hideAlert} variant="outline-success">
          Close 
        </Button>
        </div></Alert>
        <Button style={{ float:'right'}}onClick={this.handleFinishExam}   variant="success" >Finish Exam</Button>
        </div>;
        
      }
      else
      {
        FinishQuestionAlert ="";
      }
        return (
        <div>
          <div style={{display:'none'}} class="modal-custom" id="ExamFinishBox">
          <Modal.Dialog  >
              <Modal.Header >
              <Modal.Title>Exam Alert</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                Exam "{window.ExamTitleBOX}" Created Successfully
            </Modal.Body>
            <Modal.Footer>
              <Button variant="primary" onClick={event =>  window.location.href='#/instructor-home'} >Ok</Button>
            </Modal.Footer>
          </Modal.Dialog>
          </div>
          <div class="modal-custom" id="ExamtitleBox">
          <Modal.Dialog  >
              <Modal.Header >
              <Modal.Title>Exam title</Modal.Title>
              </Modal.Header>
              <Modal.Body>
                <Form.Group controlId="formExamTitle">
                <Form.Control type="text" id='TextExamTitle' placeholder="Enter Exam Title" />
                <Form.Text className="text-muted">
                Ex: Marketing Midterm Spring 2020
                </Form.Text>
                </Form.Group>
            </Modal.Body>
            <Modal.Footer>
              <Button variant="primary" onClick={this.handleConfirm} >Confirm</Button>
            </Modal.Footer>
          </Modal.Dialog>
          </div>
              
    <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
        <br />
    <Form id="ExamForm" style={{backgroundColor:'white'}}>
  <Form.Group controlId="formQuestionType">
    <Form.Label>Question Type</Form.Label>
    <Row>
    <Form.Control id="QuestionType" as="select" style={{width:'35%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Question Type</option>
    <option>MCQ</option>
    <option>Complete</option>
    <option>T and F</option>
    <option>Essay Question</option>
    <option hidden>Comparison</option>
    </Form.Control>
    <Button variant="primary" id="QuestionTypeBtn" onClick={this.handleSubmit} type="submit">Submit</Button>
   

    </Row>
    <Form.Text className="text-muted">
      Note: You can change Question Type at anytime from above
    </Form.Text>

    {FinishQuestionAlert}

  </Form.Group>
  
  <Form.Group  style={{display:'none'}} id="formExamMCQ" controlId="formExamMCQ">
 
    <Form.Label>Multiple Choice Question</Form.Label>
    <Row>
    <Form.Control id="MCQILO"  size="sm" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
  <Form.Control   id="MCQGrade" size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextMCQuestion" type="text" placeholder="Enter Your Question" />
    <br />
    <Form.Control  size="sm" id="formChoiceTextbox" type="text" placeholder="Enter a Choice" />
    <Button  size="sm" variant="primary" onClick={this.handleAddChoice}>Add Choice</Button>
    <Button id="btnDeleteChoice"  size="sm" variant="danger" onClick={this.handleDeleteChoice}>Delete Choice</Button>
    <div id="ChoicesDiv"></div>
    <Form.Control size="sm" as="select" id="ChoiceModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    </Form.Control>
    <Button style={{ float:'right'}} variant="success" onClick={()=>{this.SubmitMCQ(window.ExamTitleBOX, document.getElementById('TextMCQuestion').value, window.ExamMCQChoices, 
      document.getElementById('ChoiceModelAns').value, document.getElementById('MCQGrade').value,document.getElementById('MCQILO').value)
      }}>Finish Question</Button>
  </Form.Group>


  <Form.Group style={{display:'none'}} id="formExamComplete" controlId="formExamComplete">
   
    <Form.Label>Complete Question</Form.Label>
    <Row>
    <Form.Control id="CompILO"  size="sm" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
  <Form.Control id="CompGrade" size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextComplete1" type="text" placeholder="Enter Your 1st part of the Question *before the space*" />
    <Form.Control size="sm"id="TextComplete2" type="text" placeholder="Enter Your 2nd part of the Question *after the space*" />
    <br />
    <Form.Control size="sm" id="AnswerComplete" type="text" placeholder="Enter Your Model Answer *the space*" />
    <Button style={{ float:'right'}}variant="success"onClick={()=>{this.SubmitComplete(window.ExamTitleBOX,document.getElementById('TextComplete1').value, document.getElementById('TextComplete2').value, 
      document.getElementById('AnswerComplete').value, document.getElementById('CompGrade').value, document.getElementById('CompILO').value)}} >Finish Question</Button>
    
  </Form.Group>


  <Form.Group style={{display:'none'}} id="formExamTF" controlId="formExamTF">
    <Form.Label>True and False Question</Form.Label>
    <Row>
    <Form.Control id="TFIlo"  size="sm" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control id="TFGrade" size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextTF" type="text" placeholder="Enter Your Question" />
      <br />
      <Form.Control size="sm" as="select" id="TFModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    <option>True</option>
    <option>False</option>
    </Form.Control>
    <Button style={{ float:'right'}} variant="success" 
    onClick={ ()=>{this.SubmitTrueFalse(window.ExamTitleBOX,document.getElementById('TextTF').value , 
    document.getElementById('TFModelAns').value, document.getElementById('TFGrade').value, document.getElementById('TFIlo').value)}}>Finish Question</Button>
    
  </Form.Group>


  <Form.Group style={{display:'none'}} id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Row>
    <Form.Control id="EssILO" size="sm" type="text" style={{width:'50%',margin: '15px 15px 15px 15px'}} placeholder="Enter Question ILO"></Form.Control>
   <Form.Control id="EssGrade" size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextEssay" type="text" placeholder="Enter Your Essay Question" />
   <br />
    <Form.Control size="sm" as="textarea"id="AnswerEssay" placeholder="Enter Your Model Answer" />
    <Button style={{ float:'right'}} variant="success" 
    onClick={()=>{this.SubmitEssay(window.ExamTitleBOX,document.getElementById('TextEssay').value , 
    document.getElementById('AnswerEssay').value, document.getElementById('EssGrade').value, document.getElementById('EssILO').value)}}
    >Finish Question</Button>
    
  </Form.Group>
</Form>

 </Container>
            
          </div>
        );
    }
}

export default CreateExam;
