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
import $ from 'jquery'; 
class ExamTF extends Component {
    constructor(props) {
        super(props);
        this.state = {value:'', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetTF()
        window.TFQuestions=[];
        window.TFAnswers=[];
    }

    GetTF()
    {
        var examname=this.props.passedname
        fetch('/GetTF/'+examname+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    handleSubmit()
    {
        window.TFAnswers=[];
        var ansGroup=""
        
        for(var i=0;i<window.TFQuestions.length;i++)
        {
            ansGroup="AnswerTF" + (i+1)
            if(document.getElementById(ansGroup)!=null)
            {
                window.TFAnswers.push($(`input[name='${ansGroup}']:checked`).val());
            }
         

        }
        
      
    }

    render() {
       
        var ExamTF = this.state.QuestionList;
        window.TFQuestions=window.ExamTF;
        var name=this.props.passedname
        var TFHead = "";
        var TF = "";
        var answer="";
        if (ExamTF.length != 0) {
            TFHead = <div><Form.Label  ><b>True or False:</b></Form.Label> <Button style={{width:'21%',margin: '10px 10px 10px 10px'}} onClick={this.handleSubmit} size="sm" variant="primary" >Submit T & F</ Button>
            <br /></div>;
            TF = ExamTF.map((Question, index) => {
                answer="AnswerTF"+(index+1)
                
                return (
                    <div>
                        <Form.Label  > {index + 1})&nbsp;{ExamTF[index]}  </Form.Label>
                        <Form.Label style={{ paddingRight:"6px" ,margin:"10px 10px 10px 10px" }}><input type="radio" name={answer} id={answer}  value="True"  />True </Form.Label>   
                        <Form.Label style={{paddingRight:"6px",margin:"10px 10px 10px 10px"}}><input type="radio" name={answer} id={answer}  value="False" />False </Form.Label> 
                        
                        
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