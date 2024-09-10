'use client'
import React from 'react'
import { CheckToken } from '@/components/CheckToken'
import Sidebar from '@/components/Sidebar'

const Dashboard = () => {

  
 
  return (
    <CheckToken>
        <div>
         <div className="side">
         <div className="mover"></div>
       
          <Sidebar />


        </div>
    
    <div className="body" style={{color:"#000"}}>

        Wecome body
    </div>

    {/* <div className="per"></div> */}
    
          

         </div>
       </CheckToken>
  )
}

export default Dashboard