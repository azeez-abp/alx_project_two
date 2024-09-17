'use client'
import React, { Children } from 'react'
import { CheckToken } from '@/components/CheckToken'
import Sidebar from '@/components/Sidebar'
import AddProduct from '@/components/product/AddProduct'
import { usePathname } from 'next/navigation'
import ListProduct from '@/components/product/ListProduct'
import AddExpenditure from '@/components/expend/AddExpenditure'
import ListExpenditure from '@/components/expend/ListExpenditure'


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
                
                {pathname === '/add-product' &&  <AddProduct/> }   
                {pathname === '/list-product' &&  <ListProduct/> }  
                {pathname === '/add-expenditure' && <AddExpenditure /> } 
                {pathname === '/list-expenditure' && <ListExpenditure /> } 
               
            </div> 
         </div>
       </CheckToken>
  )
}

export default Dashboard