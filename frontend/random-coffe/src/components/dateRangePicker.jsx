import React, { useState } from 'react';
import { DateRangePicker } from 'react-date-range';
import 'react-date-range/dist/styles.css';
import 'react-date-range/dist/theme/default.css'; 
import { styles } from '../styles/dateRangePicker';
import { defaultStyles } from '../styles/default';




export const DatePickerModal = ({dateRange, setDateRange, setShowDatePicker}) => {
    const [tempDateRange, setTempDateRange] = useState(dateRange);

    const handleSaveDates = () => {
        setDateRange(tempDateRange);
        setShowDatePicker(false);
    };

    return (
        <div style={styles.modalOverlay}>
            <div style={styles.dateModalContent}>
                <h1 style={defaultStyles.title}>Выберите диапазон дат</h1>
                    <DateRangePicker
                        ranges={[tempDateRange || {
                            startDate: new Date(),
                            endDate: new Date(),
                            key: 'selection'
                        }]}
                        showPreview={false}
                        onChange={ranges => setTempDateRange(ranges.selection)}
                        minDate={new Date()}
                        rangeColors={['#1e90ff']}
                        direction="vertical"

                    />
                <div style={styles.modalButtons}>
                    <button
                        style={styles.cancelButton}
                        onClick={() => setShowDatePicker(false)}
                    >
                        Отмена
                    </button>
                    <button
                        style={styles.applyButton}
                        onClick={handleSaveDates}
                    >
                        Сохранить
                    </button>
                </div>
            </div>
        </div>
    );
};
