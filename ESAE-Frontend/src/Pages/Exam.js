// import React, { Component } from 'react';
// import { Link } from 'react-router-dom';
// import './Exam.css';
// import Card from 'react-bootstrap/Card';
// import Button from 'react-bootstrap/Button';
// import Container from 'react-bootstrap/Container';
// import Form from 'react-bootstrap/Form';
// import Row from 'react-bootstrap/Row';
// import Col from 'react-bootstrap/Col';
// import ListGroup from 'react-bootstrap/ListGroup'
// class Exam extends Component {

//     render() {
//        var names= window.ExamTitle;
//        if (names==null)
//        {
//         var nameslist='No Exams Yet'
//        }
//        else
//        {
//         var nameslist= names.map(function(ExamTitle){
//             return  <Form.Label  style={{textAlign: 'center'}} >{ExamTitle}</Form.Label>;
//           })
//        }
//     var ExamMCQ=window.ExamMCQ;
//     var ExamComplete=window.ExamComplete
//     var ExamTF=window.ExamTF
//     var ExamEssay=window.ExamEssay
//     var ExamComparison=window.ExamComparison
//     if(ExamMCQ!=null)
//     // {
//     //     for (var i=0;i<ExamMCQ.length;i+=3)
//     //     {
//     //         <Form.Label  >Question{i+1}</Form.Label>;
//     //         <Form.Label  >Choose the Correct Answer</Form.Label>;
//     //         <Form.Label>{ExamMCQ[i]}</Form.Label>;
//     //         <Form.Label>{ExamMCQ[i+1]}</Form.Label>;
//     //         <Form.Label>{ExamMCQ[i+2]}</Form.Label>;
//     //     }
        
//     // }
        
//        return (
//         <div>
   
//     <Container style={{width:'660px',height:'590px',backgroundColor:'white'}}>
//         <br />
//        <Form >{nameslist}</Form>
//     </Container>
//         </div>
//         );
//     }
// }

// export default Exam;
