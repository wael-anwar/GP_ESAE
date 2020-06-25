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

class ViewEditMCQ extends Component{
    render(){
        var ExamMCQQuestions = window.ExamMCQQuestions;
        var ExamMCQCounter = window.ExamMCQCounter;
        var ExamMCQChoices = window.ExamMCQChoices;

        var r = "";
        var i = 0;
        var MCQHead = "";
        var answer = "";
        var choicesNumber = 0;
        if (ExamMCQQuestions.length != 0) {
            MCQHead = <div><Form.Label  ><b>Choose the Correct Answer:</b></Form.Label> <br /></div>;

            r = ExamMCQChoices.map((choice, index) => {
                if (choicesNumber == 0) {
                    choicesNumber = ExamMCQCounter[i] - 1;
                    i += 1;
                    answer = "answer" + (i);
                    return (
                        <div>
                            <Form.Label  >Question {i}: {ExamMCQQuestions[i - 1]}  </Form.Label> 
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger" >Delete</ Button>
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}}href="#/instructor-edit-mcq" size="sm" variant="primary" >Edit</ Button>
                            
            
                             <br />
                            <Form.Label inline><input type="radio" name={answer} value={choice} disabled /> {choice} </Form.Label>
                            </div>
                    )
                }
                else {
                    choicesNumber -= 1;
                    return (
                        <div >
                            <Form.Label inline><input type="radio" name={answer} value={choice} disabled /> {choice} </Form.Label>
                        </div>
                    )
                }


            });

        }

        return(
            <div>
            { MCQHead }
            { r }
            </div>
        )
    }
}
export default ViewEditMCQ;