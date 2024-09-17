import React from 'react'
import Dashboard from '../dashboard/page'
import AddExpenditure from '@/components/expend/AddExpenditure'
const page = () => {
  return (
    <Dashboard  > 
      <AddExpenditure />
    </Dashboard>
  )
}

export default page