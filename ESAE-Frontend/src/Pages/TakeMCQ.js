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
import $ from 'jquery'; 

class ExamMCQ extends Component{
    
    constructor(props) {
        super(props);
        window.MCQQuestions=[];
        window.MCQAnswers=[];
      }
    handleSubmit()
    {
        window.MCQAnswers=[];
        var ansGroup=""
    
        for(var i=0;i<window.MCQQuestions.length;i++)
        {
            ansGroup="AnswerMCQ" + (i+1)
            if(document.getElementById(ansGroup)!=null)
            {
                window.MCQAnswers.push($(`input[name='${ansGroup}']:checked`).val());
            }
         

        }
        
       
    }
    render(){
        var name=this.props.passedname
        var ExamMCQQuestions = window.ExamMCQQuestions;
        var ExamMCQCounter = window.ExamMCQCounter;
        var ExamMCQChoices = window.ExamMCQChoices;
        window.MCQQuestions=window.ExamMCQQuestions;
        var r = "";
        var i = 0;
        var MCQHead = "";
        var answer = "";
        var choicesNumber = 0;
        if (ExamMCQQuestions.length != 0) {
            MCQHead = <div><Form.Label  ><b>Choose the Correct Answer:</b></Form.Label> <Button style={{width:'21%',margin: '10px 10px 10px 10px'}} onClick={this.handleSubmit} size="sm" variant="primary" >Submit MCQ</ Button> <br /></div>;

            r = ExamMCQChoices.map((choice, index) => {
                if (choicesNumber == 0) {
                    choicesNumber = ExamMCQCounter[i] - 1;
                    i += 1;
                    answer = "AnswerMCQ" + (i);
                    return (
                        <div>
                            <Form.Label  >{i})&nbsp;{ExamMCQQuestions[i - 1]}  </Form.Label> 
                    
            
                             <br />
                            <Form.Label ><input type="radio" name={answer} value={choice} id={answer} /> {choice} </Form.Label>
                            </div>
                    )
                }
                else {
                    choicesNumber -= 1;
                    return (
                        <div >
                            <Form.Label ><input type="radio" name={answer} value={choice} id={answer} /> {choice} </Form.Label>
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
export default ExamMCQ;