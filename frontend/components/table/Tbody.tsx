import React from 'react';

const Tbody: React.FC = () => {
  return (
    <div className="custom-table-body bg-white">
      <div className="table-row">
        <div className="table-cell">Product 1</div>
        <div className="table-cell">$10.00</div>
        <div className="table-cell">Electronics</div>
      </div>
      <div className="table-row">
        <div className="table-cell">Product 2</div>
        <div className="table-cell">$20.00</div>
        <div className="table-cell">Books</div>
      </div>
    </div>
  );
};

export default Tbody;
