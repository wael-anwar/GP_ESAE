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

class ViewEditMCQ extends Component{

    constructor(props) {
        super(props);
        this.state = {value: '', MCQQuestions:[], MCQCounter:[], MCQChoices:[],CorrectAnswerList:[], 
        ILOList:[], GradeList:[], Deleted:null};
        this.GetMCQ()
             
    }

    GetMCQ()
    {
        var examname=this.props.passedname
        fetch('/GetMCQ/'+examname+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({MCQQuestions : data.QuestionList, MCQCounter : data.CounterList, MCQChoices : data.AnswerList,
            CorrectAnswerList:data.CorrectAnswerList, ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    DeleteMCQ(Question)
    {
        var examname=this.props.passedname
        fetch('/DeleteMCQ/'+examname+'/'+Question)
          .then(response => response.json())
          .then(data => this.setState({Deleted : data.Deleted}));
        window.location.reload(false);
    }
    

    render(){
        var ExamMCQQuestions = this.state.MCQQuestions;
        var ExamMCQCounter = this.state.MCQCounter;
        var ExamMCQChoices = this.state.MCQChoices;

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
                    var question = ExamMCQQuestions[i - 1]
                    var exam = this.props.passedname
                    const href1 = `/#/instructor-edit-mcq?${new URLSearchParams({ exam, question }).toString()}`;
                    return (
                        <div>
                            <Form.Label  >Question {i}: {ExamMCQQuestions[i - 1]}  </Form.Label> 
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger" 
                            onClick={()=>{this.DeleteMCQ(question)}} >Delete</ Button>
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}}href={href1} size="sm" variant="primary" >Edit</ Button>
                            
            
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
export default ViewEditMCQ;