
export const styles = {
    modalOverlay: {
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        zIndex: 1000,
    },
    dateModalContent: {
        backgroundColor: '#f0f8ff',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
    },
    modalButtons: {
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem',
        marginTop: '1rem'
    },
    cancelButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        background: 'red', 
        padding: '0.5rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    applyButton: {
        flexShrink: 0,
        fontSize: '1.2rem',
        background: '#4CAF50', 
        padding: '0.5rem 1.2rem',
        borderRadius: '20px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },

};