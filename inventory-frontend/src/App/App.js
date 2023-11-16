import React, { useState } from 'react';

import ItemsList from '../ItemsList'
import AddItem from '../AddItem'

import './App.style.css';

const App = () => {
  const [refreshItemList, setRefreshItemList] = useState(false);

  const handleRefreshItemList = () => {
    setRefreshItemList((prev) => !prev);
  };

  return (
    <div className="App">
      <AddItem onAddItem={handleRefreshItemList} />
      <ItemsList key={refreshItemList}/>
    </div>
  );
}

export default App
