import React, { useEffect, useState } from 'react';
import { styles } from '../styles/menu';
import { fetchWithTokens, goToLoginPage, deleteTokens } from '../utils/auth';


const SideMenu = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [userData, setUserData] = useState({ firstName: '', lastName: '' });

  useEffect(() => {
    const token = localStorage.getItem('access_token');
    if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUserData({
          firstName: payload.first_name || '',
          lastName: payload.last_name || ''
        });
    }
  }, []);


  const MainPage = () => {
    window.location.href = '/';
  };

  const TagsPage = () => {
    window.location.href = '/tags';
  };

  const BanPage = () => {
    window.location.href = '/banned-users';
  };

  const MeetingPage = () => {
    window.location.href = '/meetings';
  };

  const SearchProfilePage = () => {
    window.location.href = '/profile';
  };

  const logout = async () => {
    await fetchWithTokens('POST', 'http://localhost:8000/api/auth/token/revoke');
    deleteTokens();
    goToLoginPage();

  };

  const fullLogout = async () => {
    await fetchWithTokens('POST', 'http://localhost:8000/api/auth/token/revoke/all');
    deleteTokens();
    goToLoginPage();

  };

  const toggleMenu = () => setIsOpen(!isOpen);

  return (
    <>
      <button 
        onClick={toggleMenu}
        style={styles.menuButton}
        aria-label="Открыть меню"
      >
        ☰
      </button>

      <div style={{ 
        ...styles.menuOverlay,
        opacity: isOpen ? 1 : 0,
        pointerEvents: isOpen ? 'all' : 'none'
      }}>
        <div 
          style={{ 
            ...styles.menuContent,
            transform: isOpen ? 'translateX(0)' : 'translateX(100%)'
          }}
        >
          <div style={styles.menuHeader}>
            {userData.firstName} {userData.lastName}
          </div>
          
            <nav style={styles.menuNav}>
              <button style={styles.menuItem} onClick={MainPage}>Главная</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={MeetingPage}>Встречи</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={SearchProfilePage}>Профиль</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={TagsPage}>Tэги</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={BanPage}>Блокировки</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={fullLogout}>Выйти со всех устройств</button>
              <div style={styles.menuDivider} />
              <button style={styles.menuItem} onClick={logout}>Выйти</button>
            </nav>
        </div>
      </div>
    </>
  );
};

export default SideMenu;