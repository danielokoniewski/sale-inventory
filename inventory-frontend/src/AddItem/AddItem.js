import React, { useState } from 'react';
import { showNotification } from '../NotificationArea';
import './AddItem.style.css'


const AddItem = ({ onAddItem, notificationRef }) => {
  const [isFormVisible, setIsFormVisible] = useState(false);
  const [newItem, setNewItem] = useState({
    name: '',
    description: '',
    owner: '',
    expiration_date: '',
    shipping: '',
    price: '',
  });

  const handleShowForm = () => {
    setIsFormVisible(true);
  };

  const handleHideForm = () => {
    setIsFormVisible(false);
    setNewItem({
      name: '',
      description: '',
      owner: '',
      expiration_date: '',
      shipping: '',
      price: '',
    });
  };

  const handleInputChange = (field, value) => {
    setNewItem((prevItem) => ({ ...prevItem, [field]: value }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://localhost:8000/items', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(newItem),
      });

      if (response.ok) {
        // Item added successfully, hide the form
        handleHideForm();
        // Trigger a callback to fetch updated data
        onAddItem();
        showNotification(`Sucessfully added item ${newItem.name}`, 'ok', notificationRef)
      } else {
        const data = await response.json();
        const formatmessage = data.detail.map(x => `${x.loc[1]}: ${x.msg}`).join("\n")

        showNotification(`Failed to add item: ${response.status}\n${formatmessage}`, 'error', notificationRef)
      }
    } catch (error) {
      showNotification(`Error adding item: ${error}`, 'error', notificationRef)
    }
  };

  return (
    <div className="AddItem">
      <button onClick={isFormVisible ? handleHideForm : handleShowForm}>+</button>
      {isFormVisible && (
        <div className='form-container'>
          <form onSubmit={handleSubmit}>
            <p>
              <label>Name:</label>
              <input type="text" value={newItem.name} onChange={(e) => handleInputChange('name', e.target.value)} />
            </p>
            <p>
              <label>Description:</label>
              <input type="text" value={newItem.description} onChange={(e) => handleInputChange('description', e.target.value)} />
            </p>
            <p>
              <label>owner:</label>
              <input type="text" value={newItem.owner} onChange={(e) => handleInputChange('owner', e.target.value)} />
            </p>
            <p>
              <label>Expiration Date:</label>
              <input type="date" date-date-format="YYYY-MM-DD" value={newItem.expiration_date} onChange={(e) => handleInputChange('expiration_date', e.target.value)} />
            </p>

            <p>
              <label>Shipping:</label>
              <input type="text" value={newItem.shipping} onChange={(e) => handleInputChange('shipping', e.target.value)} />
            </p>

            <p>
              <label>Price:</label>
              <input type="number" value={newItem.price} onChange={(e) => handleInputChange('price', e.target.value)} />
            </p>

            <button type="submit">Submit</button>
            <button type="button" onClick={handleHideForm}>
              Cancel
            </button>
          </form>
        </div>
      )}
    </div>
  );
};

export default AddItem;