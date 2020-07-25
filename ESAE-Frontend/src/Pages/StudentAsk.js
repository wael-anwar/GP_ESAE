import React, { Component } from 'react';
//import { Link } from 'react-router-dom';
import './StudentAsk.css';
//import Card from 'react-bootstrap/Card';
import Button from 'react-bootstrap/Button';
import Container from 'react-bootstrap/Container';
//import Row from 'react-bootstrap/Row';
//import Col from 'react-bootstrap/Col';
import Form from 'react-bootstrap/Form';
//import DropdownButton from 'react-bootstrap/DropdownButton';
//import Dropdown from 'react-bootstrap/Dropdown';
class StudentAsk extends Component {

    constructor(props){
      super(props);
      this.state ={
        answer:null,
      };
      this.context = {value:""};
      this.question={value:""};
      this.dummy={value:""};
    }
    
    // async componentDidMount() {
    //   // Simple POST request with a JSON body using fetch
    //   const requestOptions = {
    //     method: 'POST'
    //   };
    //   const response = await fetch('https://jsonplaceholder.typicode.com/posts', requestOptions);
    //   const data = await response.json();
    //   this.setState({ question: data.ans });
    // }
    async answer(question){
      // console.log("Question",question)
      fetch('/model/' + question)
        .then(response => response.json())
        .then(data => this.setState({answer:data.ans}));
    }

    async setContext(context) {
      // console.log("Context", context)
      fetch('/context/' + context)
        .then(response => response.json())
        .then(data => this.dummy=data.context);
    }
    render() {

      console.log(this.state)
        return (
          <div>
            <Container
              style={{
                width: "660px",
                height: "590px",
                backgroundColor: "white"
                , overflow:'scroll'
              }}
            >
              <br />
              <Form
                style={{ backgroundColor: "white" }}                
              >
                <Form.Group id="formExamEssay" controlId="formExamEssay">
                  <Form.Label>Essay Question</Form.Label>
                  <br/><br/>
                  <Form.Label>Context</Form.Label>
                  <Form.Control
                    id="Context"
                    as="textarea"
                    name="Context"
                    placeholder="Enter Context"
                    ref={node => this.context = node}
                  />

                  <Button
                    style={{ float: "right" }}
                    variant="success"
                    onClick={() => {
                      this.setContext(this.context.value)
                    }}
                  >
                    Submit Context
                  </Button>
                  <br/>
                  <Form.Label>Question</Form.Label>

                  <Form.Control
                    id="Question"
                    as="textarea"
                    name="Question"
                    placeholder="Enter Question"   
                    ref={node => this.question=node}
                  />
                  

                  <br />
                  <Button
                    style={{ float: "right" }}
                    variant="success"
                    onClick={()=>{
                      this.answer(this.question.value)}}
                  >
                    Get Answer
                  </Button>
                  <br/>
                  <Form.Control
                    readOnly
                    value={this.state['answer']}
                  />
                </Form.Group>
              </Form>
            </Container>


          </div>
        );
    }
}

export default StudentAsk;