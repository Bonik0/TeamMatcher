export const styles = {
    meetingCard : {
      flexWrap: 'wrap',
      padding: '1.0rem',
      marginTop: '1.5rem',
      borderRadius: '12px',
      boxShadow: '0 2px 4px rgba(0,0,0,0.1)',
      backgroundColor: '#f0f8ff',
      color: '#1e90ff',
      border: '1px solid #1e90ff',
    },
    cardContent : {
      display: 'flex',
      justifyContent: 'space-between',
      padding: '1.5rem'
    },
    meetingInfo : {
      flexGrow: 1
    },
    statusBlock : { 
      marginBottom: '1.3rem' 
    },
    status : {
      textTransform: 'uppercase',
      fontSize: '1.5rem'
    },
    infoLabel : {
      display: 'block',
      fontSize: '1.4rem',
      color: '#1e90ff',
      marginBottom: '0.2rem'
    },
    datetime : { 
      fontSize: '1.5rem', 
      color: '#333' 
    },
    actionButtons : {
      display: 'flex',
      gap: '0.5rem',
      alignItems: 'center'
    },
    cancelButton : {
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
    completeButton : {
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
    participantToggle : {
      padding: '0.6rem 1.8rem',
      borderRadius: '10px',
      fontSize: '1.2rem',
      backgroundColor: '#f0f8ff',
      color: '#1e90ff',
      border: '2px solid #1e90ff',
      cursor: 'pointer',
      width: '100%',
      transition: 'all 0.2s ease',
    },

    participantsList : {
      padding: '1rem 1.2rem',
      background: '#f0f8ff',
      textAlign: 'left'
    },

    participant : {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        marginTop : '1rem'
    },
    
    participantName : {
        marginBottom: '0.3rem',
        fontSize: '1.5rem'
    },
    participantEmail : { 
      color: '#333', 
      fontSize: '1.3rem',
      wordBreak: 'break-all' 
    },

    participantActions : {
      flexShrink: 0,
      display: 'flex',
      alignItems: 'center'
    },
    banButton: {
      fontSize: '1.2rem',
      background: '#1e90ff', 
      padding: '0.5rem 0.8rem',
      borderRadius: '18px',
      border : '2px solid #e0e0e0',
      color: 'white',
      cursor: 'pointer',
      transition: 'all 0.2s ease',
    },

    bannedText : {
      color: '#1e90ff',
      fontSize: '1.2rem',
      textTransform: 'uppercase',
    }
}