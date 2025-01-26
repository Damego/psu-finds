import React from 'react';
     import { Link } from 'react-router-dom';

   import './ProfileIcon.css';
   function ProfileIcon() {
      return (
        <Link to="/profile">
            <span className="profile-icon">👤</span>
        </Link>
    );
   }
   export default ProfileIcon;