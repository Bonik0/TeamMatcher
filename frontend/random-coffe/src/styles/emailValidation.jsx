export const styles = {
    codeContainer: {
      display: 'flex',
      flexDirection: 'column',
      gap: '1rem',
      alignItems: 'center',
    },
    codeInputs: {
      display: 'flex',
      gap: '0.5rem',
      justifyContent: 'center',
    },
    codeInput: {
      width: '40px',
      height: '50px',
      textAlign: 'center',
      fontSize: '1.7rem',
      border: '2px solid #1e90ff',
      borderRadius: '5px',
    },
    resendButton: {
      background: 'none',
      border: 'none',
      color: '#1e90ff',
      cursor: 'pointer',
      fontSize: '1.1rem',
      opacity: 0.7,
      transition: 'opacity 0.2s',
      ':disabled': {
        cursor: 'not-allowed',
        opacity: 0.4,
      },
    },
  };
  