import React, { Component } from 'react';
import { Link } from 'react-router-dom';
import './Exam.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
import ExamMCQ from './ExamMCQ.js';
import ExamEssay from './ExamEssay.js';
import ExamTF from './ExamTF.js';
import ExamComplete from './ExamComplete.js';



class Exam extends Component {

    constructor(props) {
        super(props);
        
          
    }

    render() {
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');
        window.examname=name;
        return (
            <div>
    
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
        <Form.Label style={{ display: 'flex', justifyContent: 'center' }}>{name}</Form.Label>
            <ExamMCQ passedname={name} />
            <ExamTF passedname={name}/>
            <ExamComplete passedname={name}/>
            <ExamEssay passedname={name}/>
        </Form>
        </Container>
            </div>
            );
    }
}

export default Exam;
