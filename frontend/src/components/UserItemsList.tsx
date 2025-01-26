import React, { useEffect, useState } from "react";
import "./UserItemsList.css";
import { type IItem } from "src/api/types";
import { httpClient } from "src/api/client";

function UserItemsList() {
  const [items, setItems] = useState<IItem[]>(null);

  const getItems = () => {
    httpClient.getUserItems().then((res) => {
      if (res.data) {
        setItems(res.data);
      }
    });
  };

  useEffect(() => {
    getItems();
  }, []);

  const deleteItem = (item: IItem) => {
    httpClient.deleteItem(item.id).then((res) => {
      if (!res.error) {
        getItems();
      }
    });
  };

  if (items === null) {
    return;
  }

  if (!items.length) {
    return <p>У вас нет добавленных объявлений.</p>;
  }

  return (
    <div className="user-items-list">
      {items.map((item, index) => (
        <div className="item-card" key={index}>
          <img src={`http://127.0.0.1:8000/files${item.image_url}`} alt="фото" className="item-image" height={200} width={200} />
          <h3 className="item-name">{item.name}</h3>
          <div className="buttons">
            <button onClick={() => deleteItem(item)} className="delete-button">
              Удалить
            </button>
          </div>
        </div>
      ))}
    </div>
  );
}

export default UserItemsList;
