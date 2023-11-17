import React, { useState, useRef } from 'react';

import ItemsList from '../ItemsList'
import AddItem from '../AddItem'

import './App.style.css';
import NotificationArea from '../NotificationArea';

const App = () => {
  const [refreshItemList, setRefreshItemList] = useState(false);
  const notificationRef = useRef();

  const handleRefreshItemList = () => {
    setRefreshItemList((prev) => !prev);
  };

  return (
    <div className="App">
      <NotificationArea ref={notificationRef} />
      <AddItem onAddItem={handleRefreshItemList} notificationRef={notificationRef} />
      <ItemsList key={refreshItemList} notificationRef={notificationRef} />
    </div>
  );
}

export default App
