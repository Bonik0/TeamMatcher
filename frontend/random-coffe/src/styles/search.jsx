
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
    modalContent: {
        backgroundColor: '#f0f8ff',
        padding: '2rem',
        borderRadius: '10px',
        boxShadow: '0 2px 10px rgba(0, 0, 0, 0.1)',
        textAlign: 'center',
        maxWidth: '90%',
        
    },
    modalMessage: {
        fontSize: '1.7rem',
        color: '#1e90ff',
        marginBottom: '1rem',
    },
    modalButton: {
        flexShrink : 0,
        fontSize: '1.2rem',
        padding: '0.5rem 3rem',
        borderRadius: '12px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        backgroundColor: '#1e90ff',
    },
    pagination: {
        display: 'flex',
        justifyContent: 'center',
        alignItems: 'center',
        gap: '2rem',
        marginTop: '1.5rem',
    },
    pageInfo: {
        fontSize: '1.5rem',
        color: '#1e90ff'
    },
    pageButton: {
        fontSize: '1.2rem',
        display: 'inline-block',
        margin: '0.5rem',
        padding: '0.5rem 3rem',
        borderRadius: '20px',
        backgroundColor: '#f0f8ff',
        color: '#1e90ff',
        border: '2px solid #1e90ff',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    UserCard : {
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
    userInfo: {
        display: 'flex',
        justifyContent: 'space-between',
        width: '100%'
    },
    userName: {
        fontSize: '1.8rem',
        color: '#1e90ff',
        marginBottom: '0.5rem'
    },
    userEmail : { 
        fontSize: '1.5rem',
        color: '#333',
    },
    meetingBadge: {
        fontSize: '1.2rem',
        backgroundColor: '#4CAF50',
        color: 'white',
        marginLeft : '2rem',
        padding: '0.25rem 1.5rem',
        borderRadius: '18px'
    },
    actionButtons : {
        display: 'flex',
        gap: '0.5rem',
        alignItems: 'center'
    },
    dislikeButton: {
        flexShrink : 0,
        fontSize: '1.2rem',
        background: 'red', 
        padding: '0.5rem 1.2rem',
        borderRadius: '18px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    toggleSection: {
        display: 'flex',
        gap: '1rem',
        marginTop: '1rem'
    },
    toggle : {
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

    toggleList : {
        padding: '1rem 1.3rem',
        background: '#f0f8ff'
    },
    tagItem: {
        fontSize: '1.2rem',
        display: 'inline-block',
        margin: '0.5rem',
        padding: '0.8rem 1.2rem',
        borderRadius: '20px',
        backgroundColor: '#f0f8ff',
        color: '#1e90ff',
        border: '2px solid #1e90ff',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    tagName: {
        fontSize: '1.5rem',
        color: '#1e90ff'
    },
    meetingIntervals : {
        display: 'flex',
        background: '#f0f8ff',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '1rem 0rem',
    },
    datetime : { 
        fontSize: '1.5rem', 
        color: '#1e90ff' 
    },
    meetingActions : {
        flexShrink: 0,
        display: 'flex',
        alignItems: 'center'
    },
    startMeetingButton: {
        flexShrink : 0,
        fontSize: '1.2rem',
        padding: '0.5rem 1.2rem',
        borderRadius: '18px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
        background: '#4CAF50'
    },
    headerRow: {
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        marginBottom: '1rem'
    },
    advancedButton: {
        flexShrink: 0,
        fontSize: '1.5rem',
        backgroundColor : '#1e90ff',
        margin: '0.5rem',
        padding: '0.6rem 2rem',
        borderRadius: '30px',
        border : '2px solid #e0e0e0',
        color: 'white',
        cursor: 'pointer',
        transition: 'all 0.2s ease',
    },
    paramsContainer: {
        marginTop : '1.5rem',
        display: 'flex',
        flexDirection: 'column',
        gap: '1.5rem',
        width: '100%',
        marginBottom : '2rem'
    },
    paramRow: {
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        width: '100%',
        gap: '2rem',
    },
    textRow : {
        color: '#1e90ff',
        fontSize: '1.5rem',
        lex: '0 0 60%',
        textAlign: 'left',
    },
    numberInput: {
        width: '3rem',
        padding: '0.4rem 0.8rem',
        fontSize: '1.2rem',
        backgroundColor : '#f0f8ff',
        border: '2px solid #1e90ff',
        borderRadius: '10px',
        maxWidth: '150px'
    },
    checkbox: {
        width: '1.25rem',
        height: '1.25rem',
        accentColor: '#1e90ff',
        marginLeft: 'auto',
    },
    dateButton: {
        padding: '0.3rem 1.5rem',
        fontSize: '1.2rem',
        backgroundColor : '#f0f8ff',
        border: '2px solid #1e90ff',
        borderRadius: '10px',
        cursor: 'pointer',
    },
    paramControl: {
        display: 'flex',
        justifyContent: 'flex-end',
    },
    modalButtons: {
        display: 'flex',
        justifyContent: 'center',
        gap: '0.5rem'
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