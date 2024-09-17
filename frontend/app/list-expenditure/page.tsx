import React from 'react'
import Dashboard from '../dashboard/page'

import ListExpenditure from '@/components/expend/ListExpenditure'
const page = () => {
  return (
    <Dashboard  > 
      <ListExpenditure />
    </Dashboard>
  )
}

export default page