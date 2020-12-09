import React from 'react'
import Button from '@material-ui/core/Button';
import { Input } from '@material-ui/core';

export default class FileUpload extends React.Component {

  onFormSubmit(e){
    if(e){
      var buffer = e.arrayBuffer()
      let fileName = e.name()
      let ext = fileName.substring(fileName.lastIndexOf('.')+1,fileName.length)
      let url = `http://localhost:5000/update/resume`;
        authFetch(url, {
            method: 'POST',
            body: JSON.stringify({'data':buffer,'ext':ext})
        }).then(r => r.json())
            this.setState({
                file:e
            });
    }
  }
  onChange(e) {
    this.setState({file:e.target.files[0]})
  }
  
  constructor(props) {
    super(props);
    this.state ={
      file:null
    }
    this.onChange=this.onChange.bind(this)
    this.onFormSubmit=this.onFormSubmit.bind(this)
  }

  render() {
    return (
      <div>
      <form onSubmit={this.onFormSubmit}>
        <Input
        type="file"
        onChange={this.onChange}/>
        <Button
        type="submit"
        variant="contained"
        color="primary"
        style={{height: '30px', width : '100px', float:"right"}}
        >Upload</Button>
      </form>
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



