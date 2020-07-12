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

class ViewEditComplete extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[], Deleted:null};
        this.GetComplete()
        
          
    }

    GetComplete()
    {
        var examname=this.props.passedname
        fetch('/GetComplete/'+examname+'/'+window.IDToken)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    DeleteComplete(Question)
    {
        var examname=this.props.passedname
        fetch('/DeleteComplete/'+examname+'/'+Question)
          .then(response => response.json())
          .then(data => this.setState({Deleted : data.Deleted}));
        window.location.reload(false);
    }



    render() {
        var ExamComplete = this.state.QuestionList;

        var CompleteHead = "";
        var Complete = "";
        var i=0
        if (ExamComplete.length != 0) {
            CompleteHead = <div><Form.Label  ><b>Complete:</b></Form.Label> <br /></div>;
            Complete = ExamComplete.map((Question, index) => {
                if (index%2==0)
                {
                    i+=1;
                    var question = ExamComplete[index]
                    var exam = this.props.passedname
                    const href1 = `/#/instructor-edit-complete?${new URLSearchParams({ exam, question }).toString()}`;
                    return (
                        <div>
                            <Form.Label  >Question {i}: </Form.Label> 
                            <Form.Label>  {ExamComplete[index]}   </Form.Label>
                            <input type="text" placeholder="Complete.." value={this.state.CorrectAnswerList[index]} disabled style={{margin:"6px"}}/>

                            
                            <Row>
                            <Form.Label style={{width:'50%',margin: '15px 15px 15px 15px'}}> ILO:{this.state.ILOList[index]}  </Form.Label>
                            <Form.Label style={{width:'40%',margin: '15px 15px 15px 15px'}}> Grade:{this.state.GradeList[index]} </Form.Label>
                            </Row>
                            

                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger" 
                            onClick={()=>{this.DeleteComplete(question)}} >Delete</ Button>
                            <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} href={href1} size="sm" variant="primary">Edit</ Button>
                            <br>
                            </br>
                            <br>
                            </br>
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

export default ViewEditComplete;