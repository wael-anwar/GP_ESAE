import Modal from 'react-bootstrap/Modal'
import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './ViewExams.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'
import Form from 'react-bootstrap/Form';

class Popup extends Component {
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
render(){
    return(
        <Modal.Dialog id="ExamtitleBox">
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
    )
  
}
  
}

export default Popup;
