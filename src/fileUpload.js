import React from 'react'
import {authFetch} from "./auth";
import Button from '@material-ui/core/Button';
import { Input } from '@material-ui/core';

export default class FileUpload extends React.Component {

  submitResume(){
    const data = new FormData()
    data.append('file',this.state.file)
    let url = `http://localhost:5000/Resumes`;
      authFetch(url, {
            method: 'POST',
            body: data
        }).then(r => r.json()).then(()=>{
            this.setState(this.state);}
        );}

  onChange(e) {
    this.setState({file:e.target.files[0],resume:this.state.resume,resumeLink:this.state.resumeLink})
  }
  
  constructor(props) {
    super(props);
    this.state ={
      file:null,
      resume:null,
      resumeLink:null
    }
    this.onChange=this.onChange.bind(this)
    this.submitResume=this.submitResume.bind(this)
  }


  componentDidMount() {
    let url = `http://localhost:5000/Resumes`;
        authFetch(url, {
            method: 'GET',
        })
            .then(response => response.json())
            .then(
                (data) => {
                  if(data){
                    this.setState({
                      file:null,
                      resume: data,
                      resumeLink: base64ToLink(data['resume_data'],data['resume_extension'])
                  });
                  }
                },
                (error) => {
                    this.setState({
                        error
                    });
                }
            );
  }


  render() {
    return (
      <div>
        <Button
        variant="contained"
        color="primary"
        style={{height: '30px', width : '190px', marginLeft:"5px", float:"right"}}
        link={this.state.resumeLink}
        >Download Resume</Button>
        <Input type="file" onChange={this.onChange}/>
        <Button
        type="submit"
        variant="contained"
        color="primary"
        style={{height: '30px', width : '100px', float:"right"}}
        onClick={this.submitResume}
        >Upload</Button>
      </div>
   )
  }
}

//Used to render resume
function base64ToLink(base64, ext) {
  let binaryString = window.atob(base64);
  let binaryLen = binaryString.length;
  let bytes = new Uint8Array(binaryLen);
  for (let i = 0; i < binaryLen; i++) {
      let ascii = binaryString.charCodeAt(i);
      bytes[i] = ascii;
  }
  let blob = new Blob([bytes], {type: `application/${ext}`});
  return window.URL.createObjectURL(blob);
}



