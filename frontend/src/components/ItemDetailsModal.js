import React from 'react';
import './ItemDetailsModal.css';
import ModalOverlay from "./ModalOverlay";

function ItemDetailsModal({ isOpen, onClose, item }) {
    if (!isOpen || !item) return null;
    return (
       <ModalOverlay onClose={onClose}>
             <div className="modal">
                 <h2>{item.name}</h2>
                 {item.image && (
                     <img src={URL.createObjectURL(item.image)} alt="фото" className="item-image" />
                  )}
                 <p>{item.description}</p>
                 <div className="buttons">
                    <button onClick={onClose} className="close-button">Закрыть</button>
                 </div>
            </div>
      </ModalOverlay>
    );
}

export default ItemDetailsModal;