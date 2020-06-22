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
import Modal from 'react-bootstrap/Modal'
class CreateExam extends Component {
    
    constructor(props) {
        super(props);
        this.state = {value: ''};
        window.ExamTitle=[];
        window.ExamMCQ=[];
        window.ExamComplete=[];
        window.ExamTF=[];
        window.ExamEssay=[];
        window.ExamComparsion=[];

        this.handleChange = this.handleChange.bind(this);
  
        this.handleSubmit = this.handleSubmit.bind(this);
      }
      handleChange (event) {
        this.setState({value: event.target.value});
      }
      
      handleSubmit(event)
      {
        if (this.state.value=='MCQ')
        {
            document.getElementById('formExamMCQ').style.display='block';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
            document.getElementById('formExamCompare').style.display='none';
            window.ChoiceCounter=0;
            
        }
        if (this.state.value=='Complete')
        {
            document.getElementById('formExamComplete').style.display='block';
            document.getElementById('formExamMCQ').style.display='none';
            document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
            document.getElementById('formExamCompare').style.display='none';
        }
        if (this.state.value=='T and F')
        {
          document.getElementById('formExamTF').style.display='block';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamMCQ').style.display='none';
            document.getElementById('formExamEssay').style.display='none';
            document.getElementById('formExamCompare').style.display='none';
        }
        if (this.state.value=='Essay Question')
        {
          document.getElementById('formExamEssay').style.display='block';
          document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamMCQ').style.display='none';
            document.getElementById('formExamCompare').style.display='none';
        }
        if (this.state.value=='Comparison')
        {
          document.getElementById('formExamCompare').style.display='block';
          document.getElementById('formExamEssay').style.display='none';
          document.getElementById('formExamTF').style.display='none';
            document.getElementById('formExamComplete').style.display='none';
            document.getElementById('formExamMCQ').style.display='none';
        }
        
      }
      handleAddChoice()
      { 
        
        var x = document.createElement("div");
        x.setAttribute("class", "form-check form-check-inline");
        x.innerHTML='<input type="radio" class="form-check-input">'+
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
        var y=document.getElementById('choice'+window.ChoiceCounter);
        document.getElementById('ChoicesDiv').removeChild(y);
        window.ChoiceCounter--;
      }
      handleFinishQuestion()
      {
        if (document.getElementById('QuestionType').value=='MCQ')
        {
     
          window.ExamMCQ.push(document.getElementById('TextMCQuestion').value)
          for(var i=0;i<window.ChoiceCounter;i++)
          {
            
            window.ExamMCQ.push(document.getElementById('choice'+i).textContent)
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
        if (document.getElementById('QuestionType').value=='Comparison')
        {
          window.ExamComparison.push(document.getElementById('TextComparison').value)
        }
      
      }
     
      handleFinishExam()
      {
        
        window.ExamTitle.push(document.getElementById('TextExamTitle').value);
        alert( window.ExamTitle);

      }
      handleConfirm()
      {
          
          if (document.getElementById('TextExamTitle').value=="")
          {
              alert("You Must Enter an Exam Title First !")
          }
          else
          {
              //send post request with exam title
              document.getElementById('ExamtitleBox').style.display='none';
          }
          
      }
    render() {
        return (
          
        <div>
          <div class="modal-custom" id="ExamtitleBox">
          <Modal.Dialog  >
              <Modal.Header closeButton>
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
              
          
         
    <Container style={{width:'660px',height:'590px',backgroundColor:'white'}}>
        <br />
    <Form onSubmit={this.handleSubmit} style={{backgroundColor:'white'}}>

  <Form.Group controlId="formQuestionType">
    <Form.Label>Question Type</Form.Label>
    <Row>
    <Form.Control id="QuestionType" as="select" style={{width:'35%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Question Type</option>
    <option>MCQ</option>
    <option>Complete</option>
    <option>T and F</option>
    <option>Essay Question</option>
    <option>Comparison</option>
    </Form.Control>
    <Button variant="primary" type="submit">Submit</Button>
   

    </Row>
    <Form.Text className="text-muted">
      Note: You can change Question Type at anytime from above
    </Form.Text>

    

  </Form.Group>
  
  <Form.Group style={{display:'none'}} id="formExamMCQ" controlId="formExamMCQ">
 
    <Form.Label>Multiple Choice Question</Form.Label>
    <Row>
   <Form.Control  size="sm" as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Related ILO</option>
    </Form.Control>
    <Form.Control  size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextMCQuestion" type="text" placeholder="Enter Your Question" />
    <br />
    <Form.Control size="sm" id="formChoiceTextbox" type="text" placeholder="Enter a Choice" />
    <Button  size="sm" variant="primary" onClick={this.handleAddChoice}>Add Choice</Button>
    <Button id="btnDeleteChoice"  size="sm" variant="danger" onClick={this.handleDeleteChoice}>Delete Choice</Button>
    <div id="ChoicesDiv"></div>
    <Form.Control size="sm" as="select" id="ChoiceModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    </Form.Control>
    <Button size="sm" variant="success" onClick={this.handleFinishQuestion}>Finish Question</Button>
    <Button style={{ float:'right'}} onClick={this.handleFinishExam}  variant="success" >Finish Exam</Button>
  
  </Form.Group>





  <Form.Group style={{display:'none'}} id="formExamComplete" controlId="formExamComplete">
   
    <Form.Label>Complete Question</Form.Label>
    <Row>
   <Form.Control size="sm" as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Related ILO</option>
    </Form.Control>
    <Form.Control size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextComplete1" type="text" placeholder="Enter Your 1st part of the Question *before the space*" />
    <Form.Control size="sm"id="TextComplete2" type="text" placeholder="Enter Your 2nd part of the Question *after the space*" />
    <br />
    <Form.Control size="sm" type="text" placeholder="Enter Your Model Answer *the space*" />
    <Button size="sm" variant="success"onClick={this.handleFinishQuestion} >Finish Question</Button>
    <Button style={{ float:'right'}} onClick={this.handleFinishExam}  variant="success" >Finish Exam</Button>
  </Form.Group>

  <Form.Group style={{display:'none'}} id="formExamTF" controlId="formExamTF">
    <Form.Label>True and False Question</Form.Label>
    <Row>
   <Form.Control size="sm" as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Related ILO</option>
    </Form.Control>
    <Form.Control size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextTF" type="text" placeholder="Enter Your Question" />
      <br />
      <Form.Control size="sm" as="select" id="TFModelAns" placeholder="Choose Model Answer">
    <option>Choose Model Answer</option>
    <option>True</option>
    <option>False</option>
    </Form.Control>
    <Button size="sm" variant="success" onClick={this.handleFinishQuestion}>Finish Question</Button>
    <Button style={{ float:'right'}}onClick={this.handleFinishExam}   variant="success" >Finish Exam</Button>
  </Form.Group>


  <Form.Group style={{display:'none'}} id="formExamEssay" controlId="formExamEssay">
    <Form.Label>Essay Question</Form.Label>
    <Row>
   <Form.Control size="sm" as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Related ILO</option>
    </Form.Control>
    <Form.Control size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextEssay" type="text" placeholder="Enter Your Essay Question" />
   <br />
    <Form.Control size="sm" as="textarea" placeholder="Enter Your Model Answer" />
    <Button size="sm" variant="success" onClick={this.handleFinishQuestion}>Finish Question</Button>
    <Button style={{ float:'right'}}onClick={this.handleFinishExam}   variant="success" >Finish Exam</Button>
  </Form.Group>

  <Form.Group style={{display:'none'}} id="formExamCompare" controlId="formExamCompare">
    <Form.Label>Comparison Question</Form.Label>
    <Row>
   <Form.Control size="sm" as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}} value={this.state.value} onChange={this.handleChange} placeholder="Choose Question Type">
    <option>Choose Related ILO</option>
    </Form.Control>
    <Form.Control size="sm" style={{width:'40%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Your Grade" />
   
   </Row>
    <Form.Control size="sm" id="TextComparison" type="text" placeholder="Enter Your Compare Question" />
    <br />
    <Form.Control size="sm" as="textarea" placeholder="Enter Your Model Answer for the 1st Compare Element" />
    <Form.Control size="sm" as="textarea" placeholder="Enter Your Model Answer for the 2st Compare Element" />
    <Button size="sm" variant="success"onClick={this.handleFinishQuestion} >Finish Question</Button>
    <Button style={{ float:'right'}}onClick={this.handleFinishExam}   variant="success" >Finish Exam</Button>
  </Form.Group>



</Form>

 </Container>
            
          </div>
        );
    }
}

export default CreateExam;
