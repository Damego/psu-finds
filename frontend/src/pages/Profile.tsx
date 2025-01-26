import React, { useState, useContext } from "react";
import { AuthContext } from "../context/AuthContext";
import AuthForm from "../components/AuthForm";
import "./Profile.css";
import ModalOverlay from "../components/ModalOverlay";
import UserItemsList from "../components/UserItemsList";
import { httpClient } from "src/api/client";

function Profile() {
  const { user, setUserData } = useContext(AuthContext);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isLogin, setIsLogin] = useState(true);
  const [editMode, setEditMode] = useState(false);
  const [profileUsername, setProfileUsername] = useState(user?.name);

  const handleOpenModal = (type: boolean) => {
    setIsLogin(type);
    setIsModalOpen(true);
  };

  const handleCloseModal = () => {
    setIsModalOpen(false);
  };

  const handleEditMode = () => {
    setEditMode(true);
  };

  const handleSaveProfile = () => {
    httpClient.updateMe({ name: profileUsername }).then((res) => {
      if (res.data) {
        setUserData(res.data);
      }
    });
    setEditMode(false);
  };

  return (
    <div className="profile-page">
      <h2>Личный кабинет</h2>
      {user ? (
        <div className="profile-info">
          {editMode ? (
            <div className="edit-profile">
              <div className="form-group">
                <label htmlFor="username">Имя пользователя</label>
                <input
                  type="text"
                  id="username"
                  value={profileUsername}
                  onChange={(e) => setProfileUsername(e.target.value)}
                />
              </div>
              <div className="buttons">
                <button onClick={handleSaveProfile} className="save-button">
                  Сохранить
                </button>
                <button
                  onClick={() => setEditMode(false)}
                  className="cancel-button"
                >
                  Отменить
                </button>
              </div>
            </div>
          ) : (
            <>
              <p>
                <strong>Email:</strong> {user.email}
              </p>
              <p>
                <strong>Имя пользователя:</strong> {user.name}
              </p>

              <div className="buttons">
                <button onClick={handleEditMode} className="edit-button">
                  Редактировать профиль
                </button>
                <button
                  onClick={() => setUserData(null)}
                  className="logout-button"
                >
                  Выйти
                </button>
              </div>
            </>
          )}
          <UserItemsList />
        </div>
      ) : (
        <div className="profile-actions">
          <button
            onClick={() => handleOpenModal(true)}
            className="login-button"
          >
            Войти
          </button>
          <button
            onClick={() => handleOpenModal(false)}
            className="register-button"
          >
            Зарегистрироваться
          </button>
        </div>
      )}
      {isModalOpen && (
        <ModalOverlay onClose={handleCloseModal}>
          <AuthForm isLogin={isLogin} onClose={handleCloseModal} />
        </ModalOverlay>
      )}
    </div>
  );
}
export default Profile;
