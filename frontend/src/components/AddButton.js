import React, { useContext, useState } from "react";
import "./AddButton.css";
import AddItemModal from "./AddItemModal";

function AddButton({ onAddItem, user }) {
  const [isModalOpen, setIsModalOpen] = useState(false);

  const handleOpenModal = () => {
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  if (!user) return;

  return (
    <>
      <button className="add-button" onClick={handleOpenModal}>
        +
      </button>
      <AddItemModal
        isOpen={isModalOpen}
        onClose={handleCloseModal}
        onAddItem={onAddItem}
        user={user}
      />
    </>
  );
}
export default AddButton;
