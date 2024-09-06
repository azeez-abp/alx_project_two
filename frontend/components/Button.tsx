import React from 'react'
import Border from './Border'

const style_button  = {
    minWidth: '13em',
    height: '38px',
    background: '#0ff',
    padding: 0,
    margin: 0,
    borderRadius: '3px'
}
 

const Button = ({...props}) => {
    console.log(props)
  return (
        <Border styles_border={{border: "1.5px solid #fff"}} >
            <button className='button' onClick={props.onclick?props.onclick:()=>console.log("No function call")} style={{...style_button, ...props.styles_button}}>
                {props.name} {props.children?props.children:''}
                  
            </button>
        </Border>
  )
}

export default Button