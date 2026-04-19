export const defaultStyles = {
    container: {
      display: 'flex',
      justifyContent: 'center',
      alignItems: 'center',
      minHeight: '100vh',
      backgroundColor: '#f0f8ff',
    },
    card: {
      border : '2px solid #e0e0e0',
      backgroundColor: 'white',
      padding: '2rem',
      borderRadius: '10px',
      boxShadow: '0 2px 10px rgba(0,0,0,0.1)',
      width: '450px',
      textAlign: 'center',
      marginTop: '-50px', 
    },
    title: {
      color: '#1e90ff',
      margin: '0 0 0.5rem 0', 
      fontSize: '2rem',
      textAlign: 'center'
    },
    form: {
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
    },
    input: {
      padding: '0.8rem',
      border: '2px solid #1e90ff',
      borderRadius: '5px',
      fontSize: '1.2rem',
      width: '100%',
      outline: 'none',
      transition: 'border-color 0.3s ease',
      borderColor : '#1e90ff',
      boxSizing: 'border-box',
    },
    button: {
      backgroundColor: '#1e90ff',
      color: 'white',
      padding: '1.2rem',
      border: 'none',
      borderRadius: '5px',
      cursor: 'pointer',
      fontSize: '1.1rem',
      transition: 'background-color 0.3s',
    },
    error: {
      color: 'red',
      fontSize: '1.2rem',
      textAlign: 'center',
      margin: '0 0 1.2rem 0',
      transition: 'all 0.2s ease-out',
      opacity: 0,
      transform: 'translateY(-10px)',
      visibility: 'hidden',
    },
    errorVisible: {
      opacity: 1,
      transform: 'translateY(0)',
      visibility: 'visible',
    },
    loading: {
      textAlign: 'center',
      fontSize: '2rem',
      color: '#1e90ff',
      padding: '2rem',
    },
    noText: {
      color: '#1e90ff',
      fontSize: '1.5rem',
      textAlign: 'center',
    },
    itemsContainer: {
      display: 'flex',
      flexDirection: 'column',
      gap: '2rem',
      padding: '2rem',
      width: '85vw',
      margin: '0 auto',
      position: 'relative',
      maxWidth : '1500px'
    },
    itemsSection: {
      backgroundColor: 'white',
      borderRadius: '25px',
      padding: '1.5rem',
      border : '2px solid #e0e0e0',
      boxShadow: '0 10px 10px rgba(0,0,0,0.1)'
    }
  };
  