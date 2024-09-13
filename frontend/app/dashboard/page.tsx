'use client'
import React, { Children } from 'react'
import { CheckToken } from '@/components/CheckToken'
import Sidebar from '@/components/Sidebar'
import AddEnpend from '@/components/expend/AddEnpend'
import AddProduct from '@/components/product/AddProduct'
import { usePathname } from 'next/navigation'


const Dashboard = ({...props}) => {

  const pathname = usePathname()
  console.log(pathname, "NAME")
 
  return (
    <CheckToken  user={{'name': 'new-user'}}   login ="false">
        <div>  
         <div className="side">
         <div className="mover"></div>
        <Sidebar />
        </div>
            <div className="body h-full flex items-center justify-center" style={{color:"#000"}}>
                {pathname === '/add-expend' && <AddEnpend /> } 
                {pathname === '/add-product' &&  <AddProduct/> }   
               
            </div> 
         </div>
       </CheckToken>
  )
}

export default Dashboard