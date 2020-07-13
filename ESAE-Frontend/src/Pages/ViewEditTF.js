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

class ViewEditTF extends Component {

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[]};
        this.GetTF()
          
    }

    GetTF()
    {
        var examname=this.props.passedname
        var id = this.props.passedid
        fetch('/GetTF/'+examname+'/'+id)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
        
    }

    DeleteTF(Question)
    {
        var examname=this.props.passedname
        fetch('/DeleteTF/'+examname+'/'+Question)
          .then(response => response.json())
          .then(data => this.setState({Deleted : data.Deleted}));
        window.location.reload(false);
    }

    render() {
        var ExamTF = this.state.QuestionList;

        var TFHead = "";
        var TF = "";
        if (ExamTF.length != 0) {
            TFHead = <div><Form.Label  ><b>True or False:</b></Form.Label> <br /></div>;
            TF = ExamTF.map((Question, index) => {
                var question = ExamTF[index]
                var exam = this.props.passedname
                var id = this.props.passedid
                const href1 = `/#/instructor-edit-tf?${new URLSearchParams({ exam, question, id }).toString()}`;
                return (
                    <div>
                        <Form.Label  >Question {index + 1}: {ExamTF[index]}  </Form.Label>
                        
                        <Form.Label style={{float:"left", paddingRight:"6px"}}><input type="radio" name={index} value="False" disabled/>T </Form.Label> 
                        <Form.Label style={{ float: "left" ,paddingRight:"6px"  }}><input type="radio" name={index} value="True" disabled />F </Form.Label>
                        <Row>
                            <Form.Label style={{width:'50%',margin: '15px 15px 15px 15px'}}> ILO:{this.state.ILOList[index]}  </Form.Label>
                            <Form.Label style={{width:'40%',margin: '15px 15px 15px 15px'}}> Grade:{this.state.GradeList[index]} </Form.Label>
                        </Row>
                        <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger"
                        onClick={()=>{this.DeleteTF(question)}} >Delete</ Button>
                        <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} href={href1} size="sm" variant="primary" >Edit</ Button>
                        <br>
                        </br>
                        <br>
                        </br>
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

export default ViewEditTF;