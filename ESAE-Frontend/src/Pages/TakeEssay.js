import React, { Component } from 'react';

import './Exam.css';

import Button from 'react-bootstrap/Button';

import Form from 'react-bootstrap/Form';

class TakeEssay extends Component{
    constructor(props) {
        super(props);
        this.state = {value:'', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetEssay()
        window.EssayQuestions=[];
        window.EssayAnswers=[];
    }

    GetEssay()
    {
        var examname=this.props.passedname
        fetch('/GetEssayStud/'+examname)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
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
        var ExamEssay=this.state.QuestionList;
        window.EssayQuestions=ExamEssay;
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

export default TakeEssay;