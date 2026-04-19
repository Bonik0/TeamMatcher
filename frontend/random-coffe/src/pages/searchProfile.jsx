import React, { useState, useEffect, useCallback } from 'react';
import { parseISO } from 'date-fns';
import { v4 as uuidv4 } from 'uuid';
import { DatePickerModal } from '../components/dateRangePicker'
import { TimePicker } from '../components/timePicker';
import { defaultStyles } from '../styles/default';
import { fetchWithTokens } from '../utils/auth';
import { formatDateTime, getDateInISOformat } from '../utils/datetime';
import { styles } from '../styles/searchProfile';



const SearchProfilePage = () => {
    const [originalMinTagsMatch, setOriginalMinTagsMatch] = useState(null);
    const [minTagsMatch, setMinTagsMatch] = useState(0);
    const [meetingIntervals, setMeetingIntervals] = useState([]);
    const [selectedToRemove, setSelectedToRemove] = useState([]);
    const [showAddModal, setShowAddModal] = useState(false);
    const [error, setError] = useState(null);


    const isCorrectDate = (start, end) => {
        return !meetingIntervals.some(mi => (mi.start < end && mi.end > start && !selectedToRemove.includes(mi.id)));
    };

    const getNewDate = (date, timeStart, timeEnd) => {
        const start = new Date(date);
        start.setHours(timeStart);
        const end = new Date(date);
        if (timeEnd < timeStart) {
            end.setDate(end.getDate() + 1);
        };

        end.setHours(timeEnd);
        return [start, end];
    };

    const getBackgroundDateIntervalColor = (interval) => {
        if (selectedToRemove.includes(interval.id)){
            return 'red';
        };
        if (interval.isNew){
            return '#4CAF50';
        };
        return '#1e90ff';
    };

    const handleChangeIntervalStatus = (interval) => {
        if (selectedToRemove.includes(interval.id)){
            if (isCorrectDate(interval.start, interval.end)){
                setSelectedToRemove(selectedToRemove.filter(id => id !== interval.id));
            };
            return;
        };
        setSelectedToRemove([...selectedToRemove, interval.id]);
    };

    const handleAddIntervals = (tempDateRange, tempStartTime, tempEndTime) => {
        const newIntervals = [];
        const newIncorrectIntervalsIds = [];
        let currentDate = new Date(tempDateRange.startDate);
        let currentInterval = null;
      
        while (currentDate <= tempDateRange.endDate) {
            const [start, end] = getNewDate(currentDate, tempStartTime, tempEndTime);
            if (start >= new Date()){
                currentInterval = {
                    id: uuidv4(),
                    start : start,
                    end : end,
                    isNew: true
                };
                newIntervals.push(currentInterval);
                if (!isCorrectDate(start, end)) {
                    newIncorrectIntervalsIds.push(currentInterval.id);
                };
            };
            currentDate.setDate(currentDate.getDate() + 1);
        };

        
        setMeetingIntervals([...meetingIntervals, ...newIntervals]);
        setSelectedToRemove([...selectedToRemove, ...newIncorrectIntervalsIds]);
        setShowAddModal(false);
    };


    useEffect(() => {
        const fetchProfile = async () => {
            const response = await fetchWithTokens('GET', 'http://localhost:8000/api/search/profile/my');
            const data = await response.json();

            const initialData = data.information || {
              meeting_intervals: [],
              min_tags_match: 0
            };
            setOriginalMinTagsMatch(initialData.min_tags_match);
            setMinTagsMatch(initialData.min_tags_match);
            setMeetingIntervals(
                initialData.meeting_intervals.map(interval => ({
                    id: uuidv4(),
                    start: parseISO(interval.start),
                    end: parseISO(interval.end),
                    isNew: false
                }))
              );
          };

        fetchProfile();
    }, []);


    const hasSavedIntervals = useCallback(() => {
            return meetingIntervals.some(mi => !mi.isNew);

        }, [meetingIntervals]);



    const hasChanges = useCallback(() => {
            if (originalMinTagsMatch === null) {
                return false;
            };
          
            const intervalsChanged = meetingIntervals.some(mi => mi.isNew) || selectedToRemove.length > 0;
            const minTagsChanged = minTagsMatch !== originalMinTagsMatch;
          
            return intervalsChanged || minTagsChanged;
        }, [originalMinTagsMatch, meetingIntervals, selectedToRemove, minTagsMatch]);


    const handleSaveChanges = async () => {
        const filteredIntervals = meetingIntervals.filter(mi => !selectedToRemove.includes(mi.id));

        const response = await fetchWithTokens(
                                                'POST',
                                                'http://localhost:8000/api/search/profile/my',
                                                JSON.stringify({
                                                  min_tags_match: minTagsMatch,
                                                  meeting_intervals: filteredIntervals.map(mi => ({
                                                    start: getDateInISOformat(mi.start),
                                                    end: getDateInISOformat(mi.end)
                                                  })),
                                                })
                                            );
        if (response.status === 200){
            setMeetingIntervals(filteredIntervals.map(interval => ({
                                                      ...interval,
                                                      isNew: false
                                                  })));
            setOriginalMinTagsMatch(minTagsMatch);
            setSelectedToRemove([]);
        };
        if (response.status === 400){
            setError('Минимальное количество тэгов должно быть не больше чем Ваше количество тэгов');
        };
    };


    const handleDeleteProfile = async () => {

        await fetchWithTokens('POST', 'http://localhost:8000/api/search/profile/my/delete');

        setSelectedToRemove([]);
        setMeetingIntervals ([]);
        setOriginalMinTagsMatch(0);
        setMinTagsMatch(0);
    };


    return (
        <div style={defaultStyles.itemsContainer}>
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
            <div style={defaultStyles.itemsSection}>
                <h1 style={defaultStyles.title}>Профиль поиска</h1>
                <div style={styles.profileContent}>
                    {hasSavedIntervals() && (
                        <div style={styles.deleteProfileContainer}>
                            <button
                                style={styles.deleteProfileButton}
                                onClick={handleDeleteProfile}
                            >
                              Удалить профиль
                            </button>
                        </div>
                    )}
                    <label style={styles.label}>
                        Минимальное совпадение тегов:
                        <input
                            type="text" 
                            inputmode="numeric"
                            value={minTagsMatch}
                            onChange={(e) => setMinTagsMatch(Math.min(100, Math.max(0, parseInt(e.target.value) || 0)))}
                            style={styles.numberInput}
                        />
                    </label>
    
                
                    <div style={styles.intervalsContainer}>
                        <label style={styles.label}>Даты встреч:</label>
                        {meetingIntervals.map(mi => (
                              <button
                                  key={mi.id}
                                  style={{
                                      ...styles.intervalButton,
                                      backgroundColor : getBackgroundDateIntervalColor(mi)
                                  }}
                                  onClick={() => {handleChangeIntervalStatus(mi)}}
                              >
                                {formatDateTime({start : mi.start, end : mi.end})}
                              </button>
                            ))}
                          <button
                              style={styles.addButton}
                              onClick={() => setShowAddModal(true)}
                          >
                              + Добавить
                          </button>
                    </div>
                  
                  
                    {showAddModal && (
                        <AddNewIntervals 
                            handleAddIntervals={handleAddIntervals}
                            setShowAddModal={setShowAddModal}
                        />
                    )}
                    {hasChanges() && (
                        <button
                            style={styles.saveChangesButton}
                            onClick={handleSaveChanges}
                        >
                            Сохранить изменения
                        </button>
                    )}
                </div>
            </div>
        </div>
  );
};





const AddNewIntervals = ({handleAddIntervals, setShowAddModal}) => {
    const [showDatePicker, setShowDatePicker] = useState(false);  
    const [newDateInterval, setNewDateInterval] = useState(null);
    const [newTimeIterval, setNewTimeInterval] = useState(null);
    const [error, setError] = useState('');


    const handleSetNewDateInterval = (interval) => {
        setError('');
        setNewDateInterval(interval);
    };

    const handleTimeChange = (type, value) => {
        setNewTimeInterval(
              {
                ...newTimeIterval,
                [type]: parseInt(value)
              }
        );
    };

    const saveNewIntervals = () => {

        if (newDateInterval === null){
            setError('Дата не указана');
            return;
        };
        const startTime = newTimeIterval?.start !== undefined ? newTimeIterval.start : 0;
        const endTime = newTimeIterval?.end !== undefined ? newTimeIterval.end : 23;
        if (startTime === endTime){
            setError('Вы должны указать коректное время встречи');
            return;
        };

        setShowAddModal(false);
        handleAddIntervals(newDateInterval, startTime, endTime);
    };


    return (
        <div style={styles.modalOverlay}>
            <div style={styles.modalContent}>
                <h1 style={defaultStyles.title}>Добавление новых дат</h1>
                <div
                  style={{
                        ...defaultStyles.error,
                        ...(error && defaultStyles.errorVisible)
                      }}
                >
                    {error}
                </div>
                <div style={styles.paramsContainer}>
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Даты встречи:
                        </label>
                        <div style={styles.paramControl}>
                            <button 
                                onClick={() => setShowDatePicker(!showDatePicker)}
                                style={styles.dateButton}
                            >
                              {newDateInterval 
                                    ? `${newDateInterval.startDate.toLocaleDateString()} - ${newDateInterval.endDate.toLocaleDateString()}`
                                    : "Выберите даты"
                              }
                            </button>
                        </div>

                        {showDatePicker && 
                            <DatePickerModal 
                                dateRange={newDateInterval}
                                setDateRange={handleSetNewDateInterval}
                                setShowDatePicker={setShowDatePicker}     
                            />
                        }

                    </div>         
                    <div style={styles.paramRow}>
                        <label style={styles.textRow}>
                            Время встречи:
                        </label>
                        <TimePicker
                            timeStart={newTimeIterval?.start}
                            timeEnd={newTimeIterval?.end}
                            handleTimeStartTimeChange={(value) => handleTimeChange('start', value)}
                            handleTimeEndTimeChange={(value) => handleTimeChange('end', value)}
                        />
                    </div>
                </div>

                <div style={styles.modalButtons}>
                    <button
                      style={styles.cancelButton}
                      onClick={() => setShowAddModal(false)}
                    >
                      Отмена
                    </button>
                    <button
                      style={styles.applyButton}
                      onClick={saveNewIntervals}
                    >
                      Сохранить
                    </button>
                </div>
            </div>
        </div>
  );

};




export default SearchProfilePage;