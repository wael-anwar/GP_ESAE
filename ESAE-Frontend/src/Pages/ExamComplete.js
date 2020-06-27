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

class ExamComplete extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList1:null, QuestionList2:null, CorrectAnswerList:null, ILOList:null, GradeList:null};
        fetch('/GetComplete/'+'Marketing'+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList1 : data.QuestionList1, QuestionList2 : data.QuestionList2, 
            CorrectAnswerList : data.CorrectAnswerList, ILOList:data.ILOList, GradeList:data.GradeList}));
          
    }

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

export default ExamComplete;