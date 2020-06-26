import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Exam.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'

class ViewEditComplete extends Component {

    render() {
        var ExamComplete = window.ExamComplete;

        var CompleteHead = "";
        var Complete = "";
        var i=0
        if (ExamComplete.length != 0) {
            CompleteHead = <div><Form.Label  ><b>Complete:</b></Form.Label> <br /></div>;
            Complete = ExamComplete.map((Question, index) => {
                if (index%2==0)
                {
                    i+=1;
                    return (
                        <div>
                            <Form.Label  >Question {i}: </Form.Label> 
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger" >Delete</ Button>
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} href="#/instructor-edit-complete" size="sm" variant="primary" >Edit</ Button>
                            
                            <br/>
                            <Form.Label>  {ExamComplete[index]}   </Form.Label>
                            <input type="text" placeholder="Complete.." disabled style={{margin:"6px"}}/>
                            <Form.Label> {ExamComplete[index+1]} </Form.Label>
                        </div>
                    )
                }
            }
            );
        }

        return (
            <div>
                {CompleteHead}
                {Complete}
            </div>
        )
    }
}

export default ViewEditComplete;