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
        window.EssayQuestions=[];
        window.EssayAnswers=[];
      }
    handleSubmit()
    {
        window.EssayAnswers=[];
        
        for(var i=0;i<window.EssayCount;i++)
        {
            
            if(document.getElementById("AnswerEssay" + (i+1))!=null)
            {
                window.EssayAnswers.push(document.getElementById("AnswerEssay" + (i+1)).value);
            }

        }
        
        
    }

    render(){
        var ExamEssay=window.ExamEssay;
        window.EssayQuestions=window.ExamEssay;
        var name=this.props.passedname
        var EssayHead="";
        var Essay="";
        var answerid = "";
        if(ExamEssay.length!=0){
            EssayHead = <div><Form.Label  ><b>Essay Question(s):</b></Form.Label> <Button style={{width:'21%',margin: '10px 10px 10px 10px'}} onClick={this.handleSubmit} size="sm" variant="primary" >Submit Essay</ Button>
            <br /></div>;
            Essay= ExamEssay.map((Question,index)=>{
                window.EssayCount=index+1;
                answerid = "AnswerEssay" + (index+1);
            return(
                 <div>
                    <Form.Label  >{index+1})&nbsp;{ExamEssay[index]}  </Form.Label>
                          
                     <br />
                    <Form.Label><textarea placeholder="Enter Answer Here" id={answerid}  style={{width:"600px"}}></textarea></Form.Label>
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