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
        var ExamMCQ=window.ExamMCQ;
        var ExamComplete=window.ExamComplete;
        var ExamTF=window.ExamTF;
        var ExamEssay=window.ExamEssay;
        var ExamComparison=window.ExamComparison;
        var r="";
        var i=0;
        var MCQHead="";
        var answer="";
        if(ExamMCQ!=null)
        {
            MCQHead = <div><Form.Label  >Choose the Correct Answer:</Form.Label> <br /></div>;

            r = ExamMCQ.map((choice,index)=>{
                if(choice!="flag")
                {
                    if(ExamMCQ[index-1]=="flag")//Question 
                    {
                        i += 1;
                        return (
                            <div>
                            <Form.Label  >Question {i}: {choice}  </Form.Label>   
                            </div>
                        )
                    }
                    else{               //choices
                        answer="answer"+(i);
                        console.log("answer",answer);
                        return (
                            <div >
                                <Form.Label><input type="radio" name={answer} value={choice} disabled/> {choice} </Form.Label>
                            </div>
                        )
                    }
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
