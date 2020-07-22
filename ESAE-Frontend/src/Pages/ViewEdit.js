import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './ViewExams.css';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'
class ViewEdit extends Component {

    constructor(props) {
      super(props);
      this.state = {value: '', Exams:null, Deleted:null, id:null};
      const params = new URLSearchParams(window.location.hash.split("?")[1]);
      const ID = params.get('IDToken');
      this.state.id=ID
      fetch('/ViewExams/'+this.state.id)
        .then(response => response.json())
        .then(data => this.setState({Exams : data.ans}));
        
    }

    async FetchDelete(ExamTitle)
    {
      const response = await fetch('/DeleteExam/'+ExamTitle).then(response => response.json());
      this.setState({Deleted:response.Deleted});
    }
    async DeleteExam(ExamTitle)
    {
      await this.FetchDelete(ExamTitle)
      window.location.reload(false);
    }

    render() {
       //var names=  window.ExamTitle;
       var names = this.state.Exams
       if (names==null)
       {
        var nameslist='No Exams Yet'
       }
       else
       { 
   

        var  nameslist= names.map((name)=>{
            const ID = this.state.id
            const href1 = `/#/instructor-view-edit-exam?${new URLSearchParams({ name,ID }).toString()}`;
            return (
                
                <Row style={{ justifyContent:'space-evenly'}}>
                  <ListGroup style={{textAlign: 'center',width:'70%',margin: '10px 10px 10px 10px'}} >
                    <ListGroup.Item href="/#/instructor-exam"disabled>{name}</ListGroup.Item>
                   </ ListGroup>
                  
                 <Button style={{width:'10%',margin: '10px 10px 10px 10px'}} href={href1} size="sm" variant="primary" >Edit</ Button>
                 <Button style={{width:'10%',margin: '10px 10px 10px 10px'}} href="#" size="sm" variant="danger" 
                 onClick={()=>{this.DeleteExam(name)}} >Delete</ Button>
                </Row>
    
              
                   ) 
          })
       }
    
        
       return (
        <div>
          
          <h1>All Exams</h1>
   
    <Container style={{width:'660px',height:'550px',backgroundColor:'white', overflow:'scroll'}}>
        <br />
        {nameslist}
    </Container>
        </div>
        );
    }
}

export default ViewEdit;
