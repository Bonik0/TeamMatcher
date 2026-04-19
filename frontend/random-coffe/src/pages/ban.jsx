import React, { useState, useEffect } from 'react';
import { defaultStyles } from '../styles/default';
import { fetchWithTokens } from '../utils/auth';
import { styles } from '../styles/ban';


const BannedUsersPage = () => {
    const [bannedUsers, setBannedUsers] = useState([]);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        const fetchBannedUsers = async () => {
            const response = await fetchWithTokens('GET', 'http://localhost:8000/api/meetings/ban-user/my');
            const data = await response.json();
            setBannedUsers(data);
            setLoading(false);
        };

        fetchBannedUsers();
    }, []);

    const handleUnban = async (userId) => {
        await fetchWithTokens(
                                'POST',
                                'http://localhost:8000/api/meetings/ban-user/my/unban',
                                JSON.stringify({blocked_id : userId})
                            )
        setBannedUsers(prev => prev.filter(user => user.user_id !== userId));
    };

    if (loading) {
        return <div style={defaultStyles.loading}>Загрузка...</div>;
    }

    return (
        <div style={defaultStyles.itemsContainer}>
          <div style={defaultStyles.itemsSection}>
            <h2 style={defaultStyles.title}>Заблокированные пользователи</h2>

            {bannedUsers.length === 0 ? (
              <p style={defaultStyles.noText}>Нет заблокированных пользователей</p>
            ) : (
                bannedUsers.map(user => (
                      <div key={user.user_id} style={styles.userCard}>
                        <div style={styles.userInfo}>
                          <div style={styles.userName}>
                            {user.first_name} {user.last_name}
                          </div>
                          <div style={styles.userEmail}>{user.email}</div>
                        </div>
                        <button
                          style={styles.unbanButton}
                          onClick={() => handleUnban(user.user_id)}
                        >
                          Разблокировать
                        </button>
                      </div>
                    ))
                )}
          </div>
        </div>
    );
};


export default BannedUsersPage;