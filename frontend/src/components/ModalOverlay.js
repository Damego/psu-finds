import React from 'react';
import './ModalOverlay.css';

function ModalOverlay({ children, onClose }) {
  return (
    <div className="modal-overlay">
        <div className="modal">
            {children}
         </div>
     </div>
  );
}

export default ModalOverlay;