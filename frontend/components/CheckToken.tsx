import { makeRequest } from '@/request'
import Link from 'next/link'
import React, { useEffect, useState } from 'react'


export const CheckToken = ({...props}) => {

  const [err__, setErr] = useState(false)
  const [hasToken, setHasToken]  = useState(false)
  const [dotNum, setDotNum]  = useState('.')
  const [message, setMessage] = useState("")

 let checkToken = async()=>{
    dotAnimate()
    makeRequest('check_token',{},(err, data)=>{
     
      if (err&&err.error){ 
        setMessage(err.message)
        return setErr(true)
      }
      
      if (data.hasOwnProperty("token"))
      { 
        setHasToken(true)
        
        localStorage.setItem('alx_token', data.token)

      }

    }, 'POST').catch(error=>{
        console.log(error) 
    })
 }

 useEffect(()=>{checkToken()}, [])
   
 let dotAnimate = async()=>{
  let initDot = dotNum
   let int =  setInterval(()=> {
      initDot+=`.`
      setDotNum(initDot)
      if (initDot.length===4) initDot = `.`
      if (hasToken) clearInterval(int)
    }, 3000)

 }
  return (
    <div 
    is-ready={hasToken?("READY"):("NOY YET")}
    >
    {!hasToken ? (
      <div className='' style={{display:'flex', alignItems:'center', justifyContent:'center',width:'100%', height:'100vh'}}>
        <div> 
             {
             message !=="" ? 
             (<>{message}  
             <Link style={{backgroundColor:"#444", color:"#fff", borderRadius:"4px", border:"1px solid", padding:"4px"}} href={"/login"}>Login</Link> </>) 
             
             : (<>We are checking your access <span>{dotNum}</span></>)

             }  
         
        </div>
      </div>
    ) : (
      !err__ && props.children
    )}
  </div>
  )
}
