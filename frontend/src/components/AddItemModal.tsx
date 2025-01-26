import React, { useState, useEffect } from "react";
import "./AddItemModal.css";
import ModalOverlay from "./ModalOverlay";
import { ItemTypes } from "src/api/enums";

function AddItemModal({ isOpen, onClose, onAddItem, user }) {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [image, setImage] = useState(null);
  const [type, setType] = useState<ItemTypes>(ItemTypes.LOST);

  useEffect(() => {
    if (!isOpen) {
      setName("");
      setDescription("");
      setImage(null);
      setType(ItemTypes.LOST);
    }
  }, [isOpen]);

  const handleSubmit = (e) => {
    e.preventDefault();
    onAddItem({
      name,
      description,
      image,
      type,
      username: user?.username || "Имя пользователя",
      profileImage: user?.profileImage,
    });
    onClose();
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    setImage(file);
  };

  if (!isOpen) return null;

  return (
    <ModalOverlay onClose={onClose}>
      <div className="modal">
        <h2>Добавить вещь</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="name">Название:</label>
            <input
              type="text"
              id="name"
              value={name}
              onChange={(e) => setName(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="description">Описание:</label>
            <textarea
              id="description"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              required
            />
          </div>
          <div className="form-group">
            <label htmlFor="image">Фото:</label>
            <input
              type="file"
              id="image"
              accept="image/*"
              onChange={handleImageChange}
            />
          </div>
          <div className="form-group">
            <label htmlFor="category">Категория:</label>
            <select
              id="category"
              value={type === ItemTypes.LOST ? "lost" : "found"}
              onChange={(e) => setType(e.target.value === "lost" ? ItemTypes.LOST : ItemTypes.FOUND)}
            >
              <option value="lost">Потерянная вещь</option>
              <option value="found">Найденная вещь</option>
            </select>
          </div>
          <div className="buttons">
            <button type="submit" className="add-item-button">
              Добавить
            </button>
            <button type="button" className="cancel-button" onClick={onClose}>
              Отменить
            </button>
          </div>
        </form>
      </div>
    </ModalOverlay>
  );
}
export default AddItemModal;
