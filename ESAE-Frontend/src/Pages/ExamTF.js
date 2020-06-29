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

class ExamTF extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetTF()
          
    }

    GetTF()
    {
        fetch('/GetTF/'+'Marketing'+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }
    render() {
        var ExamTF = window.ExamTF;

        var TFHead = "";
        var TF = "";
        if (ExamTF.length != 0) {
            TFHead = <div><Form.Label  ><b>True or False:</b></Form.Label> <br /></div>;
            TF = ExamTF.map((Question, index) => {
                return (
                    <div>
                        <Form.Label  >Question {index + 1}: {ExamTF[index]}  </Form.Label>
                              
                        <Form.Label style={{float:"right", paddingRight:"6px"}}><input type="radio" name={index} value="False" disabled/>F </Form.Label> 
                        <Form.Label style={{ float: "right" ,paddingRight:"6px"  }}><input type="radio" name={index} value="True" disabled />T </Form.Label>

                    </div>
                )
            }
            );
        }

        return (
            <div>
                {TFHead}
                {TF}
            </div>
        )
    }
}

export default ExamTF;