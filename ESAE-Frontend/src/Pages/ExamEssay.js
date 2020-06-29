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

class ExamEssay extends Component{

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetEssay()
          
    }

    GetEssay()
    {
        fetch('/GetEssay/'+'Marketing'+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }
    render(){
        //var ExamEssay=window.ExamEssay;
        var ExamEssay = this.state.QuestionList
        
        var EssayHead="";
        var Essay="";
        if(ExamEssay.length!=0){
            EssayHead = <div><Form.Label  ><b>Essay Questions:</b></Form.Label> <br /></div>;
            Essay= ExamEssay.map((Question,index)=>{
            return(
                 <div>
                    <Form.Label  >Question {index+1}: {ExamEssay[index]}  </Form.Label>
                          
                     <br />
                    <Form.Label><textarea placeholder="Answer.." disabled style={{width:"600px"}}></textarea></Form.Label>
                </div>
                )
            }
            );
        }

        return (
            <div>
                {EssayHead}
                {Essay}
            </div>
        )
    }
}

export default ExamEssay;