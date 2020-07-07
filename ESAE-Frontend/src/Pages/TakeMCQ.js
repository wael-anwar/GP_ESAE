import React, { Component } from 'react';

import './Exam.css';

import Button from 'react-bootstrap/Button';

import Form from 'react-bootstrap/Form';
import $ from 'jquery'; 

class TakeMCQ extends Component{
    
    constructor(props) {
        super(props);
        this.state = {value:'', QuestionList:[], CounterList:[], AnswerList:[],CorrectAnswerList:[], 
        ILOList:[], GradeList:[]};
        this.GetMCQ()
        window.MCQQuestions=[];
        window.MCQAnswers=[];
    }

    GetMCQ()
    {
        var examname=this.props.passedname;
      fetch('/GetMCQ/'+examname+'/'+1)
          .then(response => response.json())
          .then(data => this.setState({QuestionList:data.QuestionList, CounterList:data.CounterList, AnswerList:data.AnswerList,
            CorrectAnswerList:data.CorrectAnswerList, ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    handleSubmit()
    {
        window.MCQAnswers=[];
        var ansGroup=""
    
        for(var i=0;i<window.MCQQuestions.length;i++)
        {
            ansGroup="AnswerMCQ" + (i+1)
            if(document.getElementById(ansGroup)!=null)
            {
                window.MCQAnswers.push($(`input[name='${ansGroup}']:checked`).val());
            }
         

        }
        
       
    }
    render(){
        var name=this.props.passedname
        var ExamMCQQuestions = this.state.QuestionList;
        var ExamMCQCounter = this.state.CounterList;
        var ExamMCQChoices = this.state.AnswerList;
        ExamMCQChoices = ExamMCQChoices.toString().split(',');
        window.MCQQuestions=ExamMCQQuestions;
        var r = "";
        var i = 0;
        var MCQHead = "";
        var answer = "";
        var choicesNumber = 0;
        if (ExamMCQQuestions.length != 0) {
            MCQHead = <div><Form.Label  ><b>Choose the Correct Answer:</b></Form.Label> <Button style={{width:'21%',margin: '10px 10px 10px 10px'}} onClick={this.handleSubmit} size="sm" variant="primary" >Submit MCQ</ Button> <br /></div>;

            r = ExamMCQChoices.map((choice, index) => {
                if (choicesNumber == 0) {
                    choicesNumber = ExamMCQCounter[i] - 1;
                    i += 1;
                    answer = "AnswerMCQ" + (i);
                    return (
                        <div>
                            <Form.Label  >{i})&nbsp;{ExamMCQQuestions[i - 1]}  </Form.Label> 
                    
            
                             <br />
                            <Form.Label ><input type="radio" name={answer} value={choice} id={answer} /> {choice} </Form.Label>
                            </div>
                    )
                }
                else {
                    choicesNumber -= 1;
                    return (
                        <div >
                            <Form.Label ><input type="radio" name={answer} value={choice} id={answer} /> {choice} </Form.Label>
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
export default TakeMCQ;