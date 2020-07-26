import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './ViewExams.css';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup'
import Spinner from 'react-bootstrap/Spinner'
import Alert from 'react-bootstrap/Alert'
class ViewGrade extends Component {

  constructor(props) {
    super(props);
    this.state = {value: '', Exams:null, Grades:null, id:null};
    const params = new URLSearchParams(window.location.hash.split("?")[1]);
    const ID = params.get('IDToken');
    this.state.id=ID
    this.GetExams()
    this.GradeExam = this.GradeExam.bind(this);
      
  }
  showProgress()
  {
    document.getElementById("Progressbar").style.display='block';
  }
  GetExams()
  {
    fetch('/ViewExams/'+this.state.id)
      .then(response => response.json())
      .then(data => this.setState({Exams : data.ans}));
  }

  async FetchGrade(ExamTitle)
  {
    const response = await fetch('/GradeExam/'+ExamTitle).then(response => response.json());
    this.setState({Grades:response.Grades});
  }

  async GradeExam(ExamTitle)
  {
    await this.FetchGrade(ExamTitle);
    
    if(this.state.Grades=='dntGrade')
    {
      alert('Minimum Number of Students to Start Grading is 2 ')
    }
    else
    {
      window.GradedExam=ExamTitle
      this.showProgress();
     
    }

  }
  hideAlert(){
    document.getElementById("FinishGradingAlert").style.display="none";
  }
    render() {
        var FinishGradingAlert = "";
        if(this.state.Grades=='Finished generating the excel sheet successfully')
        {
          document.getElementById("Progressbar").style.display='none';
          
          FinishGradingAlert = <div id="FinishGradingAlert"> <Alert  key="FinishGradingAlert" variant='success'>Successfully Finished Grading '{window.GradedExam}' Exam <div className="d-flex justify-content-end">
            <Button onClick={this.hideAlert} variant="outline-success">
              Close 
            </Button>
            </div></Alert>
            </div>
            
        }
          else
          {
            FinishGradingAlert ="";
          }
        
      
       var names= this.state.Exams
       if (names==null)
       {
        var nameslist='No Exams Yet'
       }
       else
       { 
   

           var nameslist= names.map((name)=>{
            return (
                
                <Row style={{ justifyContent:'space-evenly'}}>
                  <ListGroup style={{textAlign: 'center',width:'80%',margin: '10px 10px 10px 10px'}} >
                    <ListGroup.Item href="/#/instructor-exam"disabled>{name}</ListGroup.Item>
                   </ ListGroup>
                 <Button style={{width:'10%',margin: '10px 10px 10px 10px'}} size="sm" variant="success" onClick={()=>this.GradeExam(name)} >Grade</ Button>
               
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
        <Row style={{justifyContent:'center'}}>
      <Spinner style={{display:'none'}} id="Progressbar" animation="border" variant="primary" role="status">
       <span className="sr-only">Loading...</span>
        </Spinner>
      </Row>
      {FinishGradingAlert}
    </Container>
        </div>
        );
    }
}

export default ViewGrade;
