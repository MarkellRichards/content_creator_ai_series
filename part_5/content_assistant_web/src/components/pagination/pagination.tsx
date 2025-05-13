import React from 'react';

interface PaginationProps {
  total: number;
  offset: number;
  limit: number;
  setOffset: (offset: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  total,
  offset,
  limit,
  setOffset,
}) => {
  const totalPages = Math.ceil(total / limit);
  const currentPage = Math.floor(offset / limit) + 1;

  const handlePrevious = () => {
    if (offset > 0) {
      setOffset(offset - limit);
    }
  };

  const handleNext = () => {
    if (offset + limit < total) {
      setOffset(offset + limit);
    }
  };

  return (
    <div className="flex justify-between items-center my-4">
      <button
        disabled={currentPage === 1}
        onClick={handlePrevious}
        className="px-4 py-2 bg-violet-500 rounded hover:bg-violet-700 disabled:bg-violet-400 text-gray-200"
      >
        Previous
      </button>
      <span>
        Page {currentPage} of {totalPages}
      </span>
      <button
        disabled={offset + limit >= total}
        onClick={handleNext}
        className="px-4 py-2 bg-violet-500 rounded hover:bg-violet-700 disabled:bg-violet-400 text-gray-200"
      >
        Next
      </button>
    </div>
  );
};

export default Pagination;
