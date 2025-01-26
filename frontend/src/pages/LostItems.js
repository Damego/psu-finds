import React, { useState } from 'react';
import './ItemsGrid.css';
import ItemDetailsModal from '../components/ItemDetailsModal';
import cameraIcon from '../assets/camera.png';

function LostItems({ items }) {
  const [selectedItem, setSelectedItem] = useState(null);

  const handleOpenModal = (item) => {
    setSelectedItem(item);
  };

  const handleCloseModal = () => {
    setSelectedItem(null);
  };

  return (
    <div>
      <h2>Потерянные вещи</h2>
      <div className="items-grid">
        {items.map((item, index) => (
          <div className="item-card" key={index} onClick={() => handleOpenModal(item)}>
            {item.image_url ? (
              <img
                src={`http://127.0.0.1:8000/files${item.image_url}`}
                alt="фото"
                className="item-image"
                width={200}
                height={200}
              />
            ) : (
              <img src={cameraIcon} alt="стандартное фото" className="item-image" />
            )}
            <h3 className="item-name">{item.name}</h3>
             {/* <div className="user-info">
                {item.profileImage && <img src={URL.createObjectURL(item.image_url)} alt="фото профиля" className="user-image" />}
                <p className="item-user">{item.username}</p>
             </div> */}
          </div>
        ))}
      </div>
        <ItemDetailsModal isOpen={!!selectedItem} onClose={handleCloseModal} item={selectedItem} />
    </div>
  );
}
export default LostItems;