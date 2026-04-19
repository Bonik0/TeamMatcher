import React, { useState, useEffect } from 'react';
import { styles } from '../styles/tags';
import { fetchWithTokens } from '../utils/auth';
import { defaultStyles } from '../styles/default';


const PAGE_SIZE = 30;

const TagsPage = () => {
  
    const [userTags, setUserTags] = useState([]);
    const [availableTags, setAvailableTags] = useState([]);
    const [selectedToAdd, setSelectedToAdd] = useState([]);
    const [selectedToRemove, setSelectedToRemove] = useState([]);
    const [loading, setLoading] = useState(true);
    const [currentUserPage, setCurrentUserPage] = useState(0);
    const [currentAvailablePage, setCurrentAvailablePage] = useState(0);

    useEffect(() => {
        const fetchTags = async () => {
            const myTagsResponse = await fetchWithTokens('GET', 'http://localhost:8000/api/tags/my');
            const myTags = await myTagsResponse.json();
            setUserTags(myTags);
            const allTagsResponse = await fetch('http://localhost:8000/api/tags', {
                                                            method: 'GET',
                                                            headers: { 'Content-Type': 'application/json' }
                                                          });
            const allTags = await allTagsResponse.json();
                                                        
            const userTagIds = myTags.map(tag => tag.tag_id);
            setAvailableTags(allTags.filter(tag => !userTagIds.includes(tag.tag_id)));
            setLoading(false);                                 
        };

          fetchTags();
      }, []);

    const handleTagClick = (tagId, isUserTag) => {
        if (isUserTag) {
          setSelectedToRemove(prev =>
            prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
          );
        } else {
          setSelectedToAdd(prev =>
            prev.includes(tagId) ? prev.filter(id => id !== tagId) : [...prev, tagId]
          );
        }
    };

    const handleSave = async () => {

        if (selectedToAdd.length > 0) {
          await fetchWithTokens('POST', 'http://localhost:8000/api/tags/my/add', JSON.stringify({ tag_ids: selectedToAdd }));
        }

        if (selectedToRemove.length > 0) {
          await fetchWithTokens('POST', 'http://localhost:8000/api/tags/my/remove', JSON.stringify({ tag_ids: selectedToRemove }));
        }

        const addedTags = availableTags.filter(tag => 
          selectedToAdd.includes(tag.tag_id)
        );

        setUserTags(prev => [
          ...prev.filter(tag => !selectedToRemove.includes(tag.tag_id)),
          ...addedTags
        ]);

        setAvailableTags(prev => [
          ...prev.filter(tag => !selectedToAdd.includes(tag.tag_id)),
          ...userTags.filter(tag => selectedToRemove.includes(tag.tag_id))
        ]);

        setSelectedToAdd([]);
        setSelectedToRemove([]);
    };


    if (loading) {
        return <div style={defaultStyles.loading}>Загрузка...</div>;
    };
    
    const visibleUserTags = userTags.slice(0, (currentUserPage + 1) * PAGE_SIZE);
    const visibleAvailableTags = availableTags.slice(0, (currentAvailablePage + 1) * PAGE_SIZE);

    const showUserMore = userTags.length > visibleUserTags.length;
    const showAvailableMore = availableTags.length > visibleAvailableTags.length;

  return (
    <div style={defaultStyles.itemsContainer}>
      <div style={defaultStyles.itemsSection}>
        <h2 style={defaultStyles.title}>Мои теги</h2>
        {visibleUserTags.length === 0 ? (
          <p style={defaultStyles.noText}>У вас нет тегов, добавьте их</p>
        ) : (
          visibleUserTags.map(tag => (
            <button
              key={tag.tag_id}
              style={{
                ...styles.tagButton,
                backgroundColor: selectedToRemove.includes(tag.tag_id) ? 'red' : '#1e90ff'
              }}
              onClick={() => handleTagClick(tag.tag_id, true)}
            >
              {tag.name}
            </button>
          ))
        )}
        {showUserMore && (
              <button
                style={styles.moreButton}
                onClick={() => setCurrentUserPage(p => p + 1)}
              >
                Показать еще
              </button>
            )}
      </div>

      <div style={defaultStyles.itemsSection}>
        <h2 style={defaultStyles.title}>Доступные теги</h2>
        {visibleAvailableTags.map(tag => (
          <button
            key={tag.tag_id}
            style={{
              ...styles.tagButton,
              backgroundColor: selectedToAdd.includes(tag.tag_id) ? '#4CAF50' : '#1e90ff'
            }}
            onClick={() => handleTagClick(tag.tag_id, false)}
          >
            {tag.name}
          </button>
        ))}
         {showAvailableMore && (
          <button
            style={styles.moreButton}
            onClick={() => setCurrentAvailablePage(p => p + 1)}
          >
            Показать еще
          </button>
        )}
      </div>

      {(selectedToAdd.length > 0 || selectedToRemove.length > 0) && (
        <button 
          style={styles.saveButton}
          onClick={handleSave}
        >
          Сохранить изменения
        </button>
      )}
    </div>
  );
};

export default TagsPage;