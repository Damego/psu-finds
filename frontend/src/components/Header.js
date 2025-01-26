import React, { useContext } from "react";
import "./Header.css";
import Navigation from "./Navigation";
import AddButton from "./AddButton";
import ProfileIcon from "./ProfileIcon";
import { AuthContext } from "../context/AuthContext";

function Header({ onAddItem }) {
  const logoUrl =
    "https://sun9-76.userapi.com/impg/v1iuPqbEaDau0e9ywNrXv8fsVY_GheQ7gl_N5A/ynCdtJYzcW4.jpg?size=604x276&quality=95&sign=7fb60136db26c2379a776ba41baf4277&type=album";
  const { user } = useContext(AuthContext);

  return (
    <header className="header">
      <div className="logo-container">
        <img src={logoUrl} alt="лого" className="logo" />
      </div>
      <Navigation />
      <div className="actions">
        <AddButton onAddItem={onAddItem} user={user} />
        <ProfileIcon />
      </div>
    </header>
  );
}
export default Header;
