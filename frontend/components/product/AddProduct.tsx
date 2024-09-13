// components/AddProduct.tsx
'use client'
import React, { useState } from 'react';
import { makeRequest } from '@/request';

const AddProduct: React.FC = ()=> {
  const [productName, setProductName] = useState('');
  const [quantity, setQuantity] = useState<number | string>(0);
  const [price, setPrice] = useState<number | string>(0);
  const [category, setCategory] = useState('');
  const [description, setDescription] = useState('');

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    const product = {
      product_name: productName,
      quantity: Number(quantity),
      price_per_unit: Number(price),
      category: category,
      description: description,
    };

    try {
        await makeRequest('product/add', product, (err, data)=>{

     }, 'post')

      setProductName('');
      setQuantity(0);
      setPrice(0);
      setCategory('');
      setDescription('');

    } catch (error) {
      alert('Error adding product');
    }
  };

   return(
      <div className="w-4/5 mx-auto p-4 bg-white shadow-md rounded-lg text-white">
      <h2 className="text-2xl font-bold mb-4 text-black ">Add New Products</h2>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block text-sm font-medium text-gray-700">Product Name</label>
          <input
            type="text"
            placeholder="Product Name"
            value={productName}
            onChange={(e) => setProductName(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Quantity</label>
          <input
            type="number"
            placeholder="Quantity"
            value={quantity}
            onChange={(e) => setQuantity(e.target.value)}
            className="mt-1 block w-full border border-gray-300 rounded-md p-2"
            required
          />
        </div>
        <div>
          <label className="block text-sm font-medium text-gray-700">Price per Unit</label>
          <input
            type="number"
            placeholder="Price per Unit"
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
        <button
          type="submit"
          className="w-full bg-blue-500 text-white py-2 px-4 rounded-md hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-opacity-50"
        >
          Add Product
        </button>
      </form>
    </div>
   )
};

export default AddProduct;
