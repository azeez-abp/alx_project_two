import React from 'react';

const Theader: React.FC = () => {
  return (
    <div className="custom-table-header bg-gray-300">
      <div className="table-row">
        <div className="table-cell">Product Name</div>
        <div className="table-cell">Price</div>
        <div className="table-cell">Category</div>
      </div>
    </div>
  );
};

export default Theader;
