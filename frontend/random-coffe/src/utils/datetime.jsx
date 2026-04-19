export const formatDateTime = (interval) => {
    const options = {
        year : 'numeric',
        month: 'numeric',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    const startDate = new Date(interval.start);
    const endDate = new Date(interval.end);

    if (startDate.getFullYear() !== endDate.getFullYear() || startDate.getMonth() !== endDate.getMonth() || startDate.getDay() !== endDate.getDay()) {
        return `${startDate.toLocaleDateString('RU-ru', options)} - ${endDate.toLocaleDateString('RU-ru', options)}`;
    };

    const endDateYear = Intl.DateTimeFormat('RU-ru', {year : 'numeric'}).format(endDate);
    const endDateMonth = Intl.DateTimeFormat('RU-ru', {month : '2-digit'}).format(endDate);
    const endDateDay = Intl.DateTimeFormat('RU-ru', {day : '2-digit'}).format(endDate);
    const endDateHour = Intl.DateTimeFormat('RU-ru', {hour : '2-digit'}).format(endDate);
    const endDateMinute = '00';
    const startDateHour = Intl.DateTimeFormat('RU-ru', {hour : '2-digit'}).format(startDate);
    const startDateMinute = '00';
  
    return `${endDateDay}.${endDateMonth}.${endDateYear} ${startDateHour}:${startDateMinute} - ${endDateHour}:${endDateMinute}`;
};



export const getDateInISOformat = (date) => {
    const tzoffset = (new Date()).getTimezoneOffset() * 60000;
    return (new Date((new Date(date)).getTime() - tzoffset)).toISOString();
};