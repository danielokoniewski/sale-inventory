import React, { useState, useEffect, useCallback } from 'react'
import { showNotification } from '../NotificationArea';
import './ItemsList.style.css'

const ItemsList = ({ notificationRef }) => {
  const [items, setItems] = useState([]);
  const [editItemId, setEditItemId] = useState(null);
  const [updatedItem, setUpdatedItem] = useState({});

  const fetchData = useCallback(async () => {
    try {
      const response = await fetch('http://localhost:8000/items');
      const data = await response.json();
      setItems(data);
    } catch (error) {
      showNotification(`Error fetching data: ${error}`, 'error', notificationRef)
    }
  }, [notificationRef]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  const handleEditClick = (itemId) => {
    setEditItemId(itemId);
    // Initialize updatedItem with the current item values
    const currentItem = items.find((item) => item.id === itemId);
    setUpdatedItem(currentItem);
  };

  const handleConfirmUpdate = async () => {
    try {
      const response = await fetch(`http://localhost:8000/items/${editItemId}`, {
        method: 'PUT',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(updatedItem),
      });

      if (response.ok) {
        // Item updated successfully, reset edit state and fetch updated data
        setEditItemId(null);
        setUpdatedItem({});
        fetchData();
        showNotification(`Sucessfully updated item ${editItemId}`, 'ok', notificationRef)
      } else {
        showNotification('Failed to update item', 'error', notificationRef)
      }
    } catch (error) {
      showNotification(`Error updating item: ${error}`, 'error', notificationRef)
    }
  };
  const handleCancelUpdate = () => {
    // Reset edit state
    setEditItemId(null);
    setUpdatedItem({});
  };

  const handleDeleteItem = async (itemId) => {
    try {
      const response = await fetch(`http://localhost:8000/items/${itemId}`, {
        method: 'DELETE',
      });

      if (response.ok) {
        // Item deleted successfully, fetch updated data
        fetchData();
        showNotification(`Successfully deleted item ${itemId}`, 'ok', notificationRef)
      } else {
        showNotification('Failed to delete item', 'error', notificationRef)
      }
    } catch (error) {
      showNotification(`Error deleting item: ${error}`, 'error', notificationRef)
    }
  };

  return (
    <div>
      <h1>Item List</h1>
      <table className="ItemList-table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Name</th>
            <th>Description</th>
            <th>Owner</th>
            <th>Expiration Date</th>
            <th>Shipping</th>
            <th>Price</th>
            <th>Action</th>
          </tr>
        </thead>
        <tbody>
          {items.map((item) => (
            <tr key={item.id}>
              <td>{item.id}</td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="text"
                    value={updatedItem.name || item.name}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, name: e.target.value }))}
                  />
                ) : (
                  item.name
                )}
              </td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="text"
                    value={updatedItem.description || item.description}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, description: e.target.value }))}
                  />
                ) : (
                  item.description
                )}
              </td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="text"
                    value={updatedItem.owner || item.owner}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, owner: e.target.value }))}
                  />
                ) : (
                  item.owner
                )}
              </td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="date"
                    value={updatedItem.expiration_date || item.expiration_date}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, expiration_date: e.target.value }))}
                  />
                ) : (
                  item.expiration_date
                )}
              </td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="text"
                    value={updatedItem.shipping || item.shipping}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, shipping: e.target.value }))}
                  />
                ) : (
                  item.shipping
                )}
              </td>
              <td>
                {editItemId === item.id ? (
                  <input
                    type="number"
                    value={updatedItem.price || item.price}
                    onChange={(e) => setUpdatedItem((prevItem) => ({ ...prevItem, price: parseFloat(e.target.value) }))}
                  />
                ) : (
                  item.price
                )}
              </td>
              <td>
                {editItemId !== item.id ? (
                  <>
                    <button onClick={() => handleEditClick(item.id)}>Edit</button>
                    <button onClick={() => handleDeleteItem(item.id)}>Delete</button>
                  </>
                ) : (
                  <>
                    <button onClick={handleConfirmUpdate}>Confirm</button>
                    <button onClick={handleCancelUpdate}>Cancel</button>
                  </>
                )}
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ItemsList