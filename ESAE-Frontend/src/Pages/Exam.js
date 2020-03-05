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
class Exam extends Component {

    render() {
        var ExamMCQQuestions=window.ExamMCQQuestions;
        var ExamMCQCounter=window.ExamMCQCounter;
        var ExamMCQChoices=window.ExamMCQChoices;
        var ExamComplete=window.ExamComplete;
        var ExamTF=window.ExamTF;
        var ExamEssay=window.ExamEssay;
        var ExamComparison=window.ExamComparison;
        var r="";
        var i=0;
        var MCQHead="";
        var answer="";
        var choicesNumber=0;
        if(ExamMCQQuestions!=null)
        {
            MCQHead = <div><Form.Label  >Choose the Correct Answer:</Form.Label> <br /></div>;

            r = ExamMCQChoices.map((choice,index)=>{
                if(choicesNumber==0)
                {
                    choicesNumber=ExamMCQCounter[i]-1;
                    i += 1;
                    answer = "answer" + (i);
                    return (
                        <div>
                        <Form.Label  >Question {i}: {ExamMCQQuestions[i-1]}  </Form.Label>  <br/>
                        <Form.Label><input type="radio" name={answer} value={choice} disabled /> {choice} </Form.Label>
 
                        </div>
                    )
                }
                else{               
                    choicesNumber-=1;
                    return (
                        <div >
                            <Form.Label><input type="radio" name={answer} value={choice} disabled/> {choice} </Form.Label>
                        </div>
                    )
                }
                         
                
            });

        }
        return (
            <div>
    
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
        {MCQHead}
        {r}
        </Form>
        </Container>
            </div>
            );
    }
}

export default Exam;
