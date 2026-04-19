export const styles = {
    menuButton: {
      position: 'fixed',
      top: '1rem',
      right: '1rem',
      zIndex: 1001,
      background: '#1e90ff',
      color: 'white',
      border: 'none',
      borderRadius: '50%',
      width: '4rem',
      height: '4rem',
      fontSize: '2.0rem',
      cursor: 'pointer',
      boxShadow: '0 2px 5px rgba(0,0,0,0.2)',
      transition: 'transform 0.3s ease',
      ':hover': {
        transform: 'scale(1.1)'
      }
    },
    menuOverlay: {
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(0,0,0,0.3)',
      zIndex: 1000,
      transition: 'opacity 0.3s ease'
    },
    menuContent: {
      position: 'fixed',
      top: 0,
      right: 0,
      width: '90vw',
      maxWidth: '500px',
      height: '100vh',
      backgroundColor: 'white',
      boxShadow: '-2px 0 5px rgba(0,0,0,0.2)',
      transition: 'transform 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
      padding: '20px'
    },
    menuHeader: {
      fontSize: '2rem',
      color: '#1e90ff',
      padding: '10px 20px',
    },
    menuNav: {
      display: 'flex',
      flexDirection: 'column',
      gap: '8px'
    },
    menuDivider: {
      height: '2px',
      backgroundColor: '#e0e0e0',
      padding: '0px 20px',
    },

    menuItem: {
      position: 'relative',
      background: 'none',
      border: 'none',
      padding: '12px 20px',
      fontSize: '1.5rem',
      color: '#333',
      textAlign: 'left',
      cursor: 'pointer',
      borderRadius: '5px',
      transition: 'all 0.2s ease'
    }
  };