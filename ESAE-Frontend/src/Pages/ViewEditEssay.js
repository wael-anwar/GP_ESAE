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

class ViewEditEssay extends Component{

    constructor(props) {
        super(props);
        this.state = {value: '', QuestionList:[], CorrectAnswerList:[], ILOList:[], GradeList:[], Deleted:null};
        this.GetEssay()
        
          
    }

    GetEssay()
    {
        var examname=this.props.passedname
        var id = this.props.passedid
        fetch('/GetEssay/'+examname+'/'+id)
          .then(response => response.json())
          .then(data => this.setState({QuestionList : data.QuestionList, CorrectAnswerList : data.CorrectAnswerList, 
            ILOList:data.ILOList, GradeList:data.GradeList}));
    }

    DeleteEssay(Question)
    {
        var examname=this.props.passedname
        fetch('/DeleteEssay/'+examname+'/'+Question)
          .then(response => response.json())
          .then(data => this.setState({Deleted : data.Deleted}));
        window.location.reload(false);
    }

    render(){
        var ExamEssay=this.state.QuestionList;
        
        var EssayHead="";
        var Essay="";
        if(ExamEssay.length!=0){
            EssayHead = <div><Form.Label  ><b>Essay Questions:</b></Form.Label> <br /></div>;
            Essay= ExamEssay.map((Question,index)=>{
                var question = ExamEssay[index]
                var exam = this.props.passedname
                var id = this.props.passedid
                //const href1 = `/#/instructor-edit-essay?${new URLSearchParams({ exam }).toString()}?${new URLSearchParams({ question }).toString()}`;
                const href1 = `/#/instructor-edit-essay?${new URLSearchParams({ exam, question, id }).toString()}`;
            return(
                 <div>
                    <Form.Label  >Question {index+1}: {ExamEssay[index]}  </Form.Label>
                    
                    <Form.Label><textarea placeholder="Enter Answer Here" value={this.state.CorrectAnswerList[index]} disabled style={{width:"600px"}}></textarea></Form.Label>

                    <Row>
                            <Form.Label style={{width:'50%',margin: '15px 15px 15px 15px'}}> ILO:{this.state.ILOList[index]}  </Form.Label>
                            <Form.Label style={{width:'40%',margin: '15px 15px 15px 15px'}}> Grade:{this.state.GradeList[index]} </Form.Label>
                    </Row>

                    <Button style={{width:'10%',margin: '10px 10px 10px 10px',float:'right'}} size="sm" variant="danger"
                    onClick={()=>{this.DeleteEssay(question)}}  >Delete</ Button>
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
                {EssayHead}
                {Essay}
            </div>
        )
    }
}

export default ViewEditEssay;