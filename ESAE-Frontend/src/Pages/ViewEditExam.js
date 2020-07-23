import React, { Component } from 'react';
<<<<<<< HEAD
import { Link } from 'react-router-dom';
import './Exam.css';
import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
import Row from 'react-bootstrap/Row';
import Col from 'react-bootstrap/Col';
import ListGroup from 'react-bootstrap/ListGroup';
=======
//import { Link } from 'react-router-dom';
import './Exam.css';
//import Card from 'react-bootstrap/Card';
//import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
import Form from 'react-bootstrap/Form';
//import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
//import ListGroup from 'react-bootstrap/ListGroup';
>>>>>>> Yousry_Evaluate
import ViewEditMCQ from './ViewEditMCQ.js';
import ViewEditEssay from './ViewEditEssay.js';
import ViewEditTF from './ViewEditTF.js';
import ViewEditComplete from './ViewEditComplete.js';



class ViewEditExam extends Component {

<<<<<<< HEAD
    render() {
=======
    constructor(props) {
        super(props);
        this.state = {value: '', Exams:null, Deleted:null, id:null};
        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        //const name = params.get('name');
        const IDToken = params.get('ID');
        this.state.id=IDToken
          
    }

    render() {

        const params = new URLSearchParams(window.location.hash.split("?")[1]);
        const name = params.get('name');
        const id = this.state.id;

>>>>>>> Yousry_Evaluate
        return (
            <div>
    
        <Container style={{width:'660px',height:'590px',backgroundColor:'white', overflow:'scroll'}}>
            <br />
        <Form>
<<<<<<< HEAD
            <ViewEditMCQ/>
            <ViewEditTF/>
            <ViewEditComplete/>
            <ViewEditEssay/>
=======
            <ViewEditMCQ passedname={name} passedid={id} />
            <br/>
            <ViewEditTF passedname={name} passedid={id} />
            <br/>
            <ViewEditComplete passedname={name} passedid={id} />
            <br/>
            <ViewEditEssay passedname={name} passedid={id} />
>>>>>>> Yousry_Evaluate
        </Form>
        </Container>
            </div>
            );
    }
}

export default ViewEditExam;
