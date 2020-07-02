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
import Exam from './Exam.js';

class ExamTF extends Component {

    render() {
       
        var ExamTF = window.ExamTF;
        var name=this.props.passedname
        var TFHead = "";
        var TF = "";
        if (ExamTF.length != 0) {
            TFHead = <div><Form.Label  ><b>True or False:</b></Form.Label> <br /></div>;
            TF = ExamTF.map((Question, index) => {
                return (
                    <div>
                        <Form.Label  >Question {index + 1}: {ExamTF[index]}  </Form.Label>
                              
                        <Form.Label style={{float:"right", paddingRight:"6px"}}><input type="radio" name={index} id="AnswerFalse" value="False" />F </Form.Label> 
                        <Form.Label style={{ float: "right" ,paddingRight:"6px"  }}><input type="radio" name={index} id="AnswerTrue" value="True"  />T </Form.Label>
                        
                        <Form.Label  >{name}</Form.Label>
                        
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