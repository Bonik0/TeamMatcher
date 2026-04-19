import React, { useState, useEffect } from 'react';
import { fetchWithTokens } from '../utils/auth';
import { defaultStyles } from '../styles/default';
import { styles } from '../styles/meetings';
import { formatDateTime } from '../utils/datetime';



function MeetingsPage() {
    const [meetings, setMeetings] = useState([]);
    const [loading, setLoading] = useState(true);
    const [bannedUsers, setBannedUsers] = useState([]);

    useEffect(() => {
        const fetchMeetings = async () => {
            const response = await fetchWithTokens('GET', 'http://localhost:8000/api/meetings/my');
            const bannedResponse = await fetchWithTokens('GET', 'http://localhost:8000/api/meetings/ban-user/my');
            const data = await response.json();
            const bannedData = await bannedResponse.json();
            setMeetings(data);
            setBannedUsers(bannedData);
            setLoading(false);
        };
      fetchMeetings();
    }, []);

    const updateMeetingStatus = (meetingId, newStatus) => {
        setMeetings(prevMeetings =>
            prevMeetings.map(meeting =>
                    meeting.meeting_id === meetingId ? { ...meeting, status: newStatus } : meeting
            )
        );
    };

    const handleUserBan = async (user) => {
        await fetchWithTokens(
                            'POST',
                            'http://localhost:8000/api/meetings/ban-user/my/ban',
                            JSON.stringify({blocked_id : user.user_id})
                        );
        
        setBannedUsers([...bannedUsers, user]);

      };

    if (loading) {
        return <div style={defaultStyles.loading}>Загрузка...</div>;
    };

    return (
      <div style={defaultStyles.itemsContainer}>
          <div style={defaultStyles.itemsSection}>
              <h1 style={defaultStyles.title}>Встречи</h1>
                {meetings.length === 0 ? (
                    <p style={defaultStyles.noText}>У вас ещё небыло встреч</p>
                    ) : (
                    meetings.map(meeting => (
                      <MeetingCard
                          key={meeting.meeting_id}
                          meeting={meeting}
                          bannedUsers={bannedUsers}
                          onUserBan={handleUserBan}
                          updateMeetingStatus={updateMeetingStatus}
                    />
                    ))
                )}
          </div>
      </div>
    );
}

function MeetingCard({ meeting, bannedUsers, onUserBan, updateMeetingStatus }) {
    const [isParticipantsVisible, setIsParticipantsVisible] = useState(false);

    const handleStatusChange = async (meetingId, newStatus) => {

        const URL = (newStatus === 'canceled' ? 
            'http://localhost:8000/api/meetings/my/cancel' : 'http://localhost:8000/api/meetings/my/complete'
        );

        const response = await fetchWithTokens('POST', URL, JSON.stringify({ meeting_id: meetingId }))

        if (response.ok) {
          updateMeetingStatus(meeting.meeting_id, newStatus);
        }
    };

    return (
        <div style={styles.meetingCard}>
          <div style={styles.cardContent}>
            <div style={styles.meetingInfo}>
              <div style={styles.statusBlock}>
                <span style={styles.infoLabel}>Статус встречи</span>
                <span style={{...styles.status,
                            color: meeting.status === 'planned' || meeting.status === 'completed' ? 
                            '#4CAF50' : 'red'
                        }}>
                  {meeting.status === 'planned' && 'Запланирована'}
                  {meeting.status === 'canceled' && 'Отменена'}
                  {meeting.status === 'completed' && 'Завершена'}
                </span>
              </div>
              <div>
                <span style={styles.infoLabel}>Дата и время</span>
                <span style={styles.datetime}>
                  {formatDateTime(meeting.meeting_datetime)}
                </span>
              </div>
            </div>
                     
            {meeting.status === 'planned' && (
              <div style={styles.actionButtons}>
                <button
                  style={styles.cancelButton}
                  onClick={() => handleStatusChange(meeting.meeting_id, 'canceled')}
                >
                  ✖ Отменить
                </button>
                <button
                  style={styles.completeButton}
                  onClick={() => handleStatusChange(meeting.meeting_id, 'completed')}
                >
                  ✓ Завершить
                </button>
              </div>
            )}
          </div>
         
          <button
            style={{...styles.participantToggle, backgroundColor : isParticipantsVisible === false ? '#f0f8ff' :'#e3f2fd'}}
            onClick={() => setIsParticipantsVisible(!isParticipantsVisible)}
          >
            Участники
          </button>
          
         
          {isParticipantsVisible && (
            <div style={styles.participantsList}>
              {meeting.users.map(user => (
                <div key={user.user_id} style={styles.participant}>
                    <div style={styles.meetingInfo}>
                      <div style={styles.participantName}>
                        {user.first_name} {user.last_name}
                      </div>
                      <div style={styles.participantEmail}>
                        {user.email}
                      </div>
                    </div>
                    <div style={styles.participantActions}>
                        {bannedUsers.some(bu => bu.user_id === user.user_id) ? (
                            <span style={styles.bannedText}>Заблокирован</span>
                        ) : (
                            <button 
                              style={styles.banButton}
                              onClick={() => onUserBan(user)}
                            >
                              Заблокировать
                            </button>
                        )}
                    </div> 
                </div>
              ))}
            </div>
          )}
        </div>
  );
}

export default MeetingsPage;
