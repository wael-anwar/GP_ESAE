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
import ViewEditMCQ from './ViewEditMCQ.js';
import ViewEditEssay from './ViewEditEssay.js';
import ViewEditTF from './ViewEditTF.js';
import ViewEditComplete from './ViewEditComplete.js';



class ViewEditExam extends Component {

    constructor(props) {
        super(props);
        
          
    }

    render() {

        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');

        return (
            <div>
    
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
            <ViewEditMCQ passedname={name}/>
            <ViewEditTF passedname={name}/>
            <ViewEditComplete passedname={name}/>
            <ViewEditEssay passedname={name}/>
        </Form>
        </Container>
            </div>
            );
    }
}

export default ViewEditExam;
