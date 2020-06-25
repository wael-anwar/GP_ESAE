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
class FromExisting extends Component {
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
    handleTopic(){}
    handleType(){}
    handleAddtoExam(){}
    handleFinishExam(){}
  
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
              
    <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
        <br />
    <Form style={{backgroundColor:'white'}}>
    <Form.Label>Now you can Randomly Select Questions According to it's Topic and Type</Form.Label>
  
  <Form.Group controlId="formQuestionType">
    <Row>
    <Form.Control   as="select" style={{width:'50%',margin: '15px 15px 15px 15px'}}  onChange={this.handleTopic} >
    <option>Choose Related Topic/ILO</option>
    </Form.Control>
    <Form.Control id="QuestionType" as="select" style={{width:'40%',margin: '15px 15px 15px 15px'}} onChange={this.handleType} placeholder="Choose Question Type">
    <option>Choose Question Type</option>
    <option>MCQ</option>
    <option>Complete</option>
    <option>T and F</option>
    <option>Essay Question</option>
    <option hidden>Comparison</option>
    </Form.Control>
    </Row>
    <Row>
   
    <Form.Control required  style={{width:'50%',margin: '15px 15px 15px 15px'}} type="number" placeholder="Enter Number of Questions Needed" />
    <Button variant="primary"style={{width:'40%',margin: '15px 15px 15px 15px'}} onClick={this.handleAddtoExam} type="primary">Add to Exam</Button>
   </Row>

   <Button style={{ float:'right'}} size="lg" onClick={this.handleFinishExam}   variant="success" >Finish Exam</Button>
  </Form.Group>
  
</Form>

 </Container>
            
          </div>
        );
    }
}

export default FromExisting;
