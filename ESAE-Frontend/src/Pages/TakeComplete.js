import React, { Component } from 'react';

import './Exam.css';

import Button from 'react-bootstrap/Button';

import Form from 'react-bootstrap/Form';

class TakeComplete extends Component {
    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetComplete()
        window.CompleteQuestions=[];
        window.CompleteAnswers=[];
    }

    GetComplete()
    {
        var examname=this.props.passedname
        fetch('/GetCompleteStud/'+examname)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    handleSubmit()
    {
        window.CompleteAnswers=[];
        for(var i=0;i<window.CompleteCount;i++)
        {
            
            if(document.getElementById("AnswerComplete" + (i+1))!=null)
            {
                window.CompleteAnswers.push(document.getElementById("AnswerComplete" + (i+1)).value);
            }

        }
        
        
    }
    render() {
        var ExamComplete = this.state.QuestionList;
        window.CompleteQuestions=ExamComplete;
        //var Examname=this.props.passedname;
        var CompleteHead = "";
        var Complete = "";
        var i=0
        if (ExamComplete.length != 0) {
            CompleteHead = <div><Form.Label style={{ color:'green'}}  ><b>Complete the following sentences:</b></Form.Label>  <Button style={{width:'21%',margin: '10px 10px 10px 10px'}} onClick={this.handleSubmit} size="sm" variant="primary" >Submit Complete</ Button>
            <br /></div>;
            Complete = ExamComplete.map((Question, index) => {
               
                // if (index%2==0)
                // {
                i+=1;
                var answerid = "AnswerComplete" + i;
                window.CompleteCount=i;
                return (
                    <div>
                        <Form.Label  > {i})&nbsp; </Form.Label> 
                        <Form.Label>  {ExamComplete[i-1]}   </Form.Label>
                        <br></br>
                        <input type="text" id={answerid} placeholder="Enter Answer Here"  style={{margin:"6px"}}/>
                        {/* <Form.Label> {ExamComplete[index+1]} </Form.Label> */}
                        
                    </div>
                )
               // }
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

export default TakeComplete;