import React from 'react';
import { NavLink } from 'react-router-dom'; // импортируем NavLink
import './Navigation.css';

function Navigation() {
return (
     <nav className="navigation">
     <NavLink to="/found" activeClassName="active">Найденные вещи</NavLink>
     <NavLink to="/lost" activeClassName="active">Потерянные вещи</NavLink>
   </nav>
  );
}
export default Navigation;