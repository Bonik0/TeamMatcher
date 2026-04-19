import React, { useState, useEffect } from 'react';
import { fetchWithTokens } from '../utils/auth';
import { defaultStyles } from '../styles/default';
import { DatePickerModal } from '../components/dateRangePicker'
import { TimePicker } from '../components/timePicker';
import { styles } from '../styles/search';
import { formatDateTime } from '../utils/datetime';

function UserSearchPage() {
    const [users, setUsers] = useState([]);
    const [tags, setTags] = useState([]);
    const [currentPage, setCurrentPage] = useState(1);
    const [update, setUpdate] = useState(false);
    const [loading, setLoading] = useState(true);
    const [isAdvancedSearchOpen, setIsAdvancedSearchOpen] = useState(false);
    const [searchParams, setSearchParams] = useState({
        minTagsMatch: 0,
        onlyNewUsers: false,
        dateRange: null,
        timeRange: null,
    });


    useEffect(() => {
        const fetchData = async () => {

            const params = new URLSearchParams({
                page: currentPage,
                min_tags_match: searchParams.minTagsMatch,
                only_new_users: searchParams.onlyNewUsers,
                ...(searchParams.dateRange && {
                    date_start: new Date(searchParams.dateRange.startDate.getTime() - (searchParams.dateRange.startDate.getTimezoneOffset() * 60000)).toISOString(),
                    date_end: new Date(searchParams.dateRange.endDate.getTime() + 86400000 - (searchParams.dateRange.endDate.getTimezoneOffset() * 60000)).toISOString()
                }),
                ...(searchParams.timeRange && {
                    time_start: searchParams.timeRange?.start !== undefined ? searchParams.timeRange.start : 0,
                    time_end: searchParams.timeRange?.end !== undefined ? searchParams.timeRange.end : 23
                })
            });
            console.log(searchParams.timeRange?.end === undefined);

            const [usersRes, tagsRes] = await Promise.all([
                fetchWithTokens('GET', `http://localhost:8000/api/search?${params}`),
                fetchWithTokens('GET', 'http://localhost:8000/api/tags')
            ]);
            const usersData = await usersRes.json();
            const tagsData = await tagsRes.json();
            setUsers(usersData);
            setTags(tagsData);
            setLoading(false);
        };
        fetchData();
    }, [currentPage, update]);


    const handlePageChange = (newPage) => {
        if (newPage > 0) {
            setCurrentPage(newPage);
        }
    };

    const handleStartAdvancedSearch = (params) => {
        setSearchParams(params);
        setCurrentPage(1);
        setUpdate(!update);
        setIsAdvancedSearchOpen(false);
    };

    if (loading) {
        return <div style={defaultStyles.loading}>Загрузка...</div>;
    };

    return (
        
        <div style={defaultStyles.itemsContainer}>
            <div style={defaultStyles.itemsSection}>
                <div style={styles.headerRow}>
                    <h1 style={defaultStyles.title}>Поиск пользователей</h1>
                    <button
                        onClick={() => setIsAdvancedSearchOpen(true)}
                        style={styles.advancedButton}
                    >
                        Расширенный поиск
                    </button>
                </div>

                {isAdvancedSearchOpen && (
                    <AdvancedSearchModal
                        searchParams={searchParams}
                        onClose={() => setIsAdvancedSearchOpen(false)}
                        onApply={handleStartAdvancedSearch}
                    />
                )}

                {users.length === 0 ? (
                    <p style={defaultStyles.noText}>Пользователи не найдены</p>
                ) : (
                        <>
                            {users.map(user => (
                                <UserCard 
                                    key={user.user_id} 
                                    user={user} 
                                    tags={tags}
                                    update={update}
                                    setUpdate={setUpdate}
                                />
                            ))}
                        </>
                    )}
                    {(users.length !== 0 || currentPage !== 1) &&
                        <div style={styles.pagination}>
                            <button
                                style={styles.pageButton}
                                onClick={() => handlePageChange(currentPage - 1)}
                                disabled={currentPage === 1}
                            >
                                Назад
                            </button>
                            <span style={styles.pageInfo}>
                                Страница {currentPage}
                            </span>
                            <button
                                style={styles.pageButton}
                                onClick={() => handlePageChange(currentPage + 1)}
                                disabled={users.length === 0}
                            >
                                Вперед
                            </button>
                        </div>
                    }
            </div>
        </div>
    );
}



const AdvancedSearchModal = ({ searchParams, onClose, onApply }) => {
    const [localParams, setLocalParams] = useState(searchParams);
    const [showDatePicker, setShowDatePicker] = useState(false);


    const handleTimeChange = (type, value) => {
        setLocalParams(prev => ({
            ...prev,
            timeRange: {
                ...prev.timeRange,
                [type]: parseInt(value)
            }
        }));
    };

    const handleDateChange = (tempDateRange) => {
        setLocalParams(prev => ({
            ...prev,
            dateRange: tempDateRange
        }));
    };

    return (
        <div style={styles.modalOverlay}>
            <div style={styles.modalContent}>
                <h2 style={defaultStyles.title}>Расширенный поиск</h2>
                <div style={styles.paramsContainer}>
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Минимальное совпадение тегов:
                        </label>
                        <input
                            type="text" 
                            inputmode="numeric"

                            value={localParams.minTagsMatch}
                            onChange={(e) => setLocalParams(prev => ({
                                ...prev,
                                minTagsMatch: Math.min(100, Math.max(0, parseInt(e.target.value) || 0))
                            }))}
                            style={styles.numberInput}
                        />
                    </div>

                
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Только новые пользователи:
                        </label>
                        <input
                            type="checkbox"
                            checked={localParams.onlyNewUsers}
                            onChange={(e) => setLocalParams(prev => ({
                                ...prev,
                                onlyNewUsers: e.target.checked
                            }))}
                            style={styles.checkbox}
                        />
                    </div>

                        
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Даты встречи:
                        </label>
                        <div style={styles.paramControl}>
                            <button 
                                onClick={() => setShowDatePicker(!showDatePicker)}
                                style={styles.dateButton}
                            >
                                {localParams.dateRange 
                                    ? `${localParams.dateRange.startDate.toLocaleDateString()} - ${localParams.dateRange.endDate.toLocaleDateString()}`
                                    : "Выберите даты"}
                            </button>
                        </div>
                                
                        {showDatePicker && 
                            <DatePickerModal 
                                setDateRange={handleDateChange}
                                dateRange={localParams.dateRange}
                                setShowDatePicker={setShowDatePicker}        
                            />
                        }

                    </div>

                    
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Время встречи:
                        </label>
                        <TimePicker
                            timeStart={localParams.timeRange?.start}
                            timeEnd={localParams.timeRange?.end}
                            handleTimeStartTimeChange={(value) => handleTimeChange('start', value)}
                            handleTimeEndTimeChange={(value) => handleTimeChange('end', value)}
                        />
                    </div>
                </div>
                            
                <div style={styles.modalButtons}>
                    <button
                        style={styles.cancelButton}
                        onClick={onClose}
                    >
                        Отмена
                    </button>
                    <button
                        style={styles.applyButton}
                        onClick={() => onApply(localParams)}
                    >
                        Начать поиск
                    </button>
                </div>
            </div>
        </div>
    );

};

function UserCard({ user, tags, update, setUpdate }) {
    const [tagsVisible, setTagsVisible] = useState(false);
    const [datesVisible, setDatesVisible] = useState(false);
    const [error, setError] = useState(null);

    
    const matchedTags = tags.filter(tag => 
        user.matched_tag_ids.includes(tag.tag_id)
    );
    const handleUserBan = async (user) => {
        await fetchWithTokens(
                            'POST',
                            'http://localhost:8000/api/meetings/ban-user/my/ban',
                            JSON.stringify({blocked_id : user.user_id})
                        );
        setUpdate(!update);
    };

    const handleTagsToggle = (tagsVisible) => {
        setTagsVisible(tagsVisible);
        setDatesVisible(false);
    };

    const handleDateToggle = (datesVisible) => {
        setDatesVisible(datesVisible);
        setTagsVisible(false);
    };
    


    const handleStartMeeting = async (user, meetingIndex) => {
        const meetingInterval = user.meeting_intervals[meetingIndex];
        const response = await fetchWithTokens(
                                'POST', 
                                'http://localhost:8000/api/meetings/my', 
                                JSON.stringify({meeting_user_id : user.user_id, meeting_datetime : meetingInterval})
                            );
        

        if (response.status === 200) {
            setUpdate(!update);
            return;
        };
        if (response.status === 400) {
            setError('Вы не можете назначить встречу на это время, так как у одного из пользователей уже запланирована встреча на этот промежуток времени');
            return;
        };
    };

    return (
        <div style={styles.UserCard}>
            {error && (
                <div style={styles.modalOverlay}>
                    <div style={styles.modalContent}>
                        <div style={styles.modalMessage}>{error}</div>
                        <button 
                            style={styles.modalButton}
                            onClick={() => setError(null)}
                        >
                            OK
                        </button>
                    </div>
                </div>
            )}
            <div style={styles.cardContent}>
                <div style={styles.userInfo}>
                    <div>
                        <div style={styles.userName}>
                            {user.first_name} {user.last_name}
                            {(user.have_planned_meeting || user.have_completed_meeting) && (
                                <span style={styles.meetingBadge}>
                                    {user.have_planned_meeting ? 'Запланировано' : 'Была встреча'}
                                </span>
                            )}
                        </div>
                        
                        <div style={styles.userEmail}>{user.email}</div>
                    </div>
                    
                    <div style={styles.actionButtons}>
                        <button
                            style={styles.dislikeButton}
                            onClick={() => handleUserBan(user)}
                        >
                            Не интересно
                        </button>
                    </div>
                </div>
            </div>

            <div style={styles.toggleSection}>
                <button
                    style={{...styles.toggle, 
                        backgroundColor: tagsVisible ? '#e3f2fd' : '#f0f8ff'}}
                    onClick={() => handleTagsToggle(!tagsVisible)}
                >
                    Совпавшие тэги ({user.matched_tags_count})
                </button>
                
                <button
                    style={{...styles.toggle,
                        backgroundColor: datesVisible ? '#e3f2fd' : '#f0f8ff'}}
                    onClick={() => handleDateToggle(!datesVisible)}
                >
                    Доступные даты ({user.meeting_intervals.length})
                </button>
            </div>

            {tagsVisible && (
                <div style={styles.toggleList}>
                    {matchedTags.map(tag => (
                        <div key={tag.tag_id} style={styles.tagItem}>
                            <span style={styles.tagName}>{tag.name}</span>
                        </div>
                    ))}
                </div>
            )}

            {datesVisible && (
                <div style={styles.toggleList}>
                    {user.meeting_intervals.map((interval, meetingIndex) => (
                    
                    <div key={meetingIndex} style={styles.meetingIntervals}>
                        
                        <span style={styles.datetime}>
                            {formatDateTime(interval)}
                        </span>
                        
                        <div style={styles.meetingActions}>
                            <button
                                style={styles.startMeetingButton}
                                onClick={() => handleStartMeeting(user, meetingIndex)}
                            >
                                Назначить встречу
                            </button>
                        </div>
                    </div>
                    ))}
                </div>
            )}
        </div>
    );
}






export default UserSearchPage;
