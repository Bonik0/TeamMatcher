export const styles = {
  passwordWrapper: {
    position: 'relative',
    width: '100%',
  },
  eyeButton: {
    position: 'absolute',
    right: '12px',
    top: '50%',
    transform: 'translateY(-50%)',
    background: 'none',
    border: 'none',
    cursor: 'pointer',
    padding: '4px',
    borderRadius: '50%',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
  },
  eyeIcon: {
    width: '24px',
    height: '24px',
    fill: '#666',
  },
  links: {
    marginTop: '1.5rem',
    display: 'flex',
    flexDirection: 'column',
    gap: '0.5rem',
  },
  link: {
    color: '#1e90ff',
    textDecoration: 'none',
    fontSize: '1.3rem',
    '&:hover': {
      textDecoration: 'underline',
    },
  },
  
};