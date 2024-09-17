// components/AddExpenditure.tsx
'use client'
import React, { useState } from 'react';
import { makeRequest } from '@/request';
import Button from '../../components/Button';



const spinner_style = {
  position: 'absolute',
  left: '17em',
  top: '-18px'
}

const AddExpenditure: React.FC = ()=> {
  const [productName, setProductName] = useState('');
  const [quantity, setQuantity] = useState<number | string>(0);
  const [price, setPrice] = useState<number | string>(0);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');
  const [buttonState, setButtonState]  = useState({
    showLoader:false,
    error:false, 
    info:"", 
    suc:false})
  const disble_button = {
    pointerEvents: buttonState.showLoader ? 'none' : 'all',
    opacity:buttonState.showLoader ? '0.4' : '1',
    cursor:buttonState.showLoader ? 'none' : 'pointer'
  }


  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setButtonState({...buttonState,showLoader:true,error:false})
    const product = {
    
      amount: Number(price),
      category: category,
      description: description,
      user_id: localStorage.getItem('alx_user_id')
    };

    try {
        await makeRequest('expenditure', product, (err, data)=>{
          if (err) return setButtonState({...buttonState,showLoader:false,error:true, info:err.message ||err.error})
          
          setButtonState({...buttonState,showLoader:false,error:false, suc:true, info:data.message})

          setProductName('');
          setQuantity(0);
          setPrice(0);
          setCategory('');
          setDescription('');
         return
           
     }, 'post')

      
    } catch (error) {
      alert('Error adding product');
    }
  };

   return(
      <div className="w-4/5 mx-auto p-4 bg-white shadow-md rounded-lg text-white">
      <h2 className="text-2xl font-bold mb-4 text-black ">Add New Expenditure</h2>
      {(buttonState.error|| buttonState.suc)  && <div role="alert" className={buttonState.error?'alert alert-error':'alert alert-success'}>
          <svg onClick={()=>setButtonState({...buttonState, error:false,suc:false})} xmlns="http://www.w3.org/2000/svg" className="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
          <span>{buttonState.info}</span>
        </div>}
      <form onSubmit={handleSubmit} className="space-y-4">
       
     
        <div>
          <label className="block text-sm font-medium text-gray-700">Amoun spent</label>
          <input
            type="number"
            placeholder="Amoun specnd"
            value={price}
            onChange={(e) => setPrice(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Category</label>
          <input
            type="text"
            placeholder="Category"
            value={category}
            onChange={(e) => setCategory(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Description</label>
          <textarea
            placeholder="Description"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
          />
        </div>
        <Button name="Sign in"  onclick={handleSubmit} styles_button={{background: "rgb(79 70 229/.4)",
              height:"28px", fontWeight: 500, position: 'relative', ...disble_button, minWidth:"100%"} } >
                <span className="loading loading-spinner loading-sm"  style = {{...spinner_style, position: "relative", display: buttonState.showLoader?"block":"none"}}></span>
          </Button> 
      </form>
    </div>
   )
};

export default AddExpenditure;
