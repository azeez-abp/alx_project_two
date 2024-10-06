'use client'
import React, { useEffect, useState } from 'react'
import { CheckToken } from '@/components/CheckToken'
import Sidebar from '@/components/Sidebar'
import AddProduct from '@/components/product/AddProduct'
import { usePathname } from 'next/navigation'
import ListProduct from '@/components/product/ListProduct'
import AddExpenditure from '@/components/expend/AddExpenditure'
import ListExpenditure from '@/components/expend/ListExpenditure'
import AddRevenue from '@/components/revenue/AddRevenue'
import ListRevenue from '@/components/revenue/ListRevenue'
import { makeRequest } from '@/request'
import { FaProductHunt, FaChartLine, FaMoneyCheckAlt } from 'react-icons/fa';
import { Bar_ } from './BarAna'

const Analystic: React.FC = () => {
  const [revenue, setRevenue] = useState<any>(null);
  const [product, setProduct] = useState<any>(null);
  const [expenses, setExpenses] = useState<any>(null);
  const [hoveredIndex, setHoveredIndex] = useState<number | null>(null); // Track hovered card index

  const fetchrevenue = async () => {
    await makeRequest('revenue', null, (err: any, data: any) => {
      if (err) return setRevenue([]);
      setRevenue(data.data);
    }, "GET");

    await makeRequest('product', null, (err: any, data: any) => {
      if (err) return setProduct([]);
      setProduct(data.data);
    }, "GET");

    await makeRequest('expenditure', null, (err: any, data: any) => {
      if (err) return setExpenses([]);
      setExpenses(data.data);
    }, "GET");
  }

  const iconFontSize = { fontSize: "40px" }
  useEffect(() => {
    fetchrevenue();
  }, []);

  const cardAnas = [
    {
      info: "Total product",
      value: product ? product.length : 0,
      icon: <FaProductHunt className="text-3xl mr-2" style={iconFontSize} />
    },
    {
      info: "Total revenue",
      value: revenue ? revenue.length : 0,
      icon: <FaMoneyCheckAlt className="text-3xl mr-2" style={iconFontSize} />
    },
    {
      info: "Total Expenses",
      value: expenses ? expenses.length : 0,
      icon: <FaChartLine className="text-3xl mr-2" style={iconFontSize} />
    },
    {
      info: "Total Amount of Product",
      value: product ? product.reduce((total, p) => ((total + p.quantity * p.price_per_unit)/1), 0) : 0,
      icon: <FaProductHunt className="text-3xl mr-2" style={iconFontSize} />
    },
    {
      info: "Total Quantity of Product",
      value: product ? product.reduce((total, p) => ((total + p.quantity)/1), 0) : 0,
      icon: <FaProductHunt className="text-3xl mr-2" style={iconFontSize} />
    },
  ];

  return (
    <div className="flex w-full flex-col px-5">
      {/* Cards */}
      <div className="w-full flex h-1/5 flex-wrap cursor-pointer">
        {cardAnas.map((cardAna, key) => (
          <div className="mb-4 p-4 bg-white shadow-lg rounded-md w-1/4 flex items-center mx-4" key={key}>
            <div className="flex items-center">
              <div className="w-1/6">{cardAna.icon}</div>
              <div style={{ position: "relative" }}>
                <div className="text-lg font-semibold w-4/6 wrap ellipsis mx-2"
                  onMouseEnter={() => setHoveredIndex(key)}
                  onMouseLeave={() => setHoveredIndex(null)}
                >
                  {cardAna.info}
                  {hoveredIndex === key && (
                    <div className="absolute left-0 mt-1 p-2 bg-gray-700 text-white rounded-md">
                      {cardAna.info}
                    </div>
                  )}
                </div>

                <div className="text-lg font-semibold w-3/6" style={{
                  margin: "0 auto",
                  fontSize: "26px",
                  position: "absolute",
                  top: "5px",
                  right: "-30px"
                }}>
                  {cardAna.value}
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex w-full justify-left items-center">
        <Bar_ data={revenue} x_axis="source" y_axis="amount" title="Amount of Revenue" subtitle="By Source" />
        <Bar_ data={product} x_axis="category" y_axis="quantity" title="Product Quantity" subtitle="By Category" />
        <Bar_ data={expenses} x_axis="category" y_axis="amount" title="Product Quantity" subtitle="By Amount" />
      </div>
    </div>
  );
}

const Dashboard: React.FC = ({ ...props }) => {
  const pathname = usePathname();
  console.log(pathname, "NAME");

  return (
    <CheckToken user={{ 'name': 'new-user' }} login="false">
      <div>
        <div className="side">
          <div className="mover"></div>
          <Sidebar />
        </div>
        <div className="body h-full flex items-center justify-center" style={{ color: "#000" }}>
          {pathname === '/add-product' && <AddProduct />}
          {pathname === '/list-product' && <ListProduct />}
          {pathname === '/add-expenditure' && <AddExpenditure />}
          {pathname === '/list-expenditure' && <ListExpenditure />}
          {pathname === '/add-revenue' && <AddRevenue />}
          {pathname === '/list-revenue' && <ListRevenue />}
          {pathname === '/dashboard' && <Analystic />}
        </div>
      </div>
    </CheckToken>
  );
}

export default Dashboard;
