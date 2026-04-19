
import React, { useState } from 'react';
import { styles } from '../styles/timePicker';



export const TimePicker = ({timeStart, timeEnd, handleTimeStartTimeChange, handleTimeEndTimeChange}) => {

    const [localStartTime, setlocalStartTime] = useState(timeStart);
    const [localEndTime, setlocalEndTime] = useState(timeEnd);


    const handleLocalTimeStartChange = (value) => {
        setlocalStartTime(value);
        handleTimeStartTimeChange(value);
    };

    const handleLocalTimeEndChange = (value) => {
        setlocalEndTime(value);
        handleTimeEndTimeChange(value);
    };


    return (
        <div style={styles.timeContainer}>
            <select
                value={localStartTime !== undefined ? localStartTime : 0}
                onChange={(e) => handleLocalTimeStartChange(e.target.value)}
                style={styles.timeSelect}
            >
                {Array.from({length: 24}, (_, i) => (
                    <option key={`start-${i}`} value={i}>
                        {i.toString().padStart(2, '0')}:00
                    </option>
                ))}
            </select>
            <span style={styles.timeSpan}> — </span>
            <select
                value={localEndTime !== undefined ? localEndTime : 23}
                onChange={(e) => handleLocalTimeEndChange(e.target.value)}
                style={styles.timeSelect}
            >
                {Array.from({length: 24}, (_, i) => (
                    <option key={`end-${i}`} value={i}>
                        {i.toString().padStart(2, '0')}:00
                    </option>
                ))}
            </select>
        </div>
    )
};






