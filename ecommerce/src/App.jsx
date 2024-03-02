// App.jsx
import React, { useState } from 'react';
import NavbarMenu from './components/Navbar';
import ProductList from './components/Productos';

const App = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');

  const handleSearch = (term) => {
    setSearchTerm(term);
  };

  const handleCategorySelect = (category) => {
    setSelectedCategory(category);
  };

  return (
    <div >
      <NavbarMenu onSearch={handleSearch} onSelectCategory={handleCategorySelect} />
      <ProductList searchTerm={searchTerm} selectedCategory={selectedCategory} />
    </div>
  );
};

export default App;
