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

class ExamMCQ extends Component{

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CounterList:[], AnswerList:[],CorrectAnswerList:[], 
        ILOList:[], GradeList:[]};
        this.GetMCQ()
          
    }

    GetMCQ()
    {
      fetch('/GetMCQ/'+'Marketing'+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList:data.QuestionList, CounterList:data.CounterList, AnswerList:data.AnswerList,
            CorrectAnswerList:data.CorrectAnswerList, ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    handleTopic(){}

    render(){
        var ExamMCQQuestions = this.state.QuestionList;
        var ExamMCQCounter   = this.state.CounterList;
        var ExamMCQChoices   = this.state.AnswerList;

        //var ExamMCQQuestions = window.ExamMCQQuestions;
        //var ExamMCQCounter = window.ExamMCQCounter;
        //var ExamMCQChoices = window.ExamMCQChoices;

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
export default ExamMCQ;