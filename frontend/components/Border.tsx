import React from 'react'
const style_border  ={
    border: '3px solid #fff',
    transition: 'border 0.2s ease-in-out',
    padding: '5px',
    display: 'flex',
    borderRadius: '4px',
    '&:hover': {
      opacity: '1' // Ensures full opacity on hover
    }
}

const Border = ({...props}) => {
  return (
    <div className='button-outline' style={{...style_border, ...props.styles_border}} >
        {props.children?props.children:<></>}
    </div>
  )
}

export default Border