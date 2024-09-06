import { makeRequest } from '@/request'
import React, { useEffect, useState } from 'react'


export const CheckToken = ({...props}) => {

  const [err__, setErr] = useState(false)

 let checkToken = ()=>{
    makeRequest('check_token',{},(err, data)=>{
        console.log(data, err)
      if (err){
       return setErr(true)
      }
      
      if (data.hasOwnProperty("refrsh_token"))
      { console.log("HAS")
        localStorage.setItem('alx_token', data.refrsh_token)

      }

    }, 'GET').catch(error=>{
        console.log(error) 
    })
 }

 useEffect(()=>{checkToken()}, [])
    
  return (
    <div> {!err__ && props.children}</div>
  )
}
