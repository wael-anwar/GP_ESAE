import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './Exam.css';
//import Card from 'react-bootstrap/Card';
//import Button from 'react-bootstrap/Button';
//import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
//import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
//import ListGroup from 'react-bootstrap/ListGroup'
//import Exam from './Exam.js';

class ExamComplete extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        //alert(window.IDToken1)
        this.GetComplete()
        
          
    }

    GetComplete()
    {
        var examname=this.props.passedname
        var id=this.props.passedid
        //alert(id)
        fetch('/GetComplete/'+examname+'/'+id)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }
    render() {
        //var ExamComplete = window.ExamComplete;
        var ExamComplete = this.state.QuestionList;

        var CompleteHead = "";
        var Complete = "";
        var i=0
        if (ExamComplete.length != 0) {
            CompleteHead = <div><Form.Label style={{ color: 'green' }} ><b>Complete the following:</b></Form.Label> <br /></div>;
            Complete = ExamComplete.map((Question, index) => {
                //if (index%2==0)
               // {
                //    i+=1;
                return (
                    <div>
                        <Form.Label  > {index + 1})&nbsp; </Form.Label> 
                        <Form.Label>  {ExamComplete[index]}   </Form.Label>
                        <br></br>
                        <input type="text" placeholder="Enter Answer Here" value={this.state.CorrectAnswerList[index]} disabled style={{margin:"6px"}}/>
                        {/* <Form.Label> {ExamComplete[index+1]} </Form.Label> */}

                    </div>
                )
                //}
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