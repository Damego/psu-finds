import React, { useState } from "react";
import "./AuthForm.css";
import { httpClient } from "src/api/client";
import { useNavigate } from "react-router-dom";
import { toast } from "react-toastify";

function AuthForm({ isLogin = true, onClose }) {
  const navigate = useNavigate();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [username, setUsername] = useState("");
  const [error, setError] = useState("");

  const handleSignIn = () => {
    httpClient.signIn(email, password).then((res) => {
      if (res.error) {
        toast(res.error.message, { type: "error" });
      } else {
        toast("Вы успешно вошли в аккаунт!", { type: "success" });
        navigate("/");
      }
    });
  };

  const handleSignUp = () => {
    httpClient.signUp(email, username, password).then((res) => {
      if (res.error) {
        toast(res.error.message, { type: "error" });
      } else {
        toast("Вы успешно зарегистрировались! Теперь войдите в аккаунт", {
          type: "success",
        });
        onClose();
      }
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    setError("");
    if (isLogin) {
      handleSignIn();
    } else {
      handleSignUp();
    }
  };

  return (
    <div className="auth-form">
      <h2>{isLogin ? "Вход" : "Регистрация"}</h2>
      {error && <p className="error-message">{error}</p>}
      <form onSubmit={handleSubmit}>
        {!isLogin && (
          <div className="form-group">
            <label htmlFor="username">Имя пользователя</label>
            <input
              type="text"
              id="username"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              required
            />
          </div>
        )}
        <div className="form-group">
          <label htmlFor="email">Email</label>
          <input
            type="email"
            id="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />
        </div>
        <div className="form-group">
          <label htmlFor="password">Пароль</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>
        <div className="buttons">
          <button type="submit" className="auth-button">
            {isLogin ? "Войти" : "Зарегистрироваться"}
          </button>
          <button type="button" className="cancel-button" onClick={onClose}>
            Отменить
          </button>
        </div>
      </form>
    </div>
  );
}
export default AuthForm;
