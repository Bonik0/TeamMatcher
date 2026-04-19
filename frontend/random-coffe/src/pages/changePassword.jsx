import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { styles } from '../styles/auth';
import { defaultStyles } from '../styles/default';
import { getAuthParams, getURLtoEmailVetify, goToLoginPage } from '../utils/auth'


const ChangePasswordPage = () => {
    
    const [opId, email] = getAuthParams();

    const [formData, setFormData] = useState({
          password: '',
          confirmPassword: ''
        });
  
    const noErrorsState = {
          email : false,
          password: false,
          confirmPassword : false,
          message: '',
      }
    const [errors, setErrors] = useState(noErrorsState);
    const [showPassword, setShowPassword] = useState(false);
    const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  
    const handleInputChange = (field, value) => {
        setFormData(prev => ({
          ...prev,
          [field]: value
        }));
    
        if (errors[field]) {
          setErrors(noErrorsState);
        }
      };
  
    const handleErrorsChange = (msg, fieldError) => {
          setErrors(          
                      {
                        ...noErrorsState,
                        [fieldError]: true,
                        message: msg
                      }
                  )
      };


    const handleSubmit = async (e) => {
        e.preventDefault();


        if (formData.password.length < 5) {
            handleErrorsChange('Пароль должен содержать минимум 5 символов', 'password');
            return;
        }


        if (formData.password !== formData.confirmPassword) {
            handleErrorsChange('Пароли не совпадают', 'confirmPassword');
            return;
        }
        const response = await fetch('http://localhost:8000/api/auth/change-password', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(
                                { 
                                    email : email,
                                    operation_id : opId,
                                    password : formData.password
                                }
                        ),
        });
        const response_dict = await response.json();

        if (response.status === 400) {
            const type = response_dict['detail']['type'];
            if (type === 'access_blocked') {
                window.location.href = getURLtoEmailVetify(window.location.pathname, email);
                return;
            }
        };

        if (response.status === 200) {
            goToLoginPage();
            return;
        };
    
    
  };

  return (
    <div style={defaultStyles.container}>
      <div style={defaultStyles.card}>
        <h2 style={defaultStyles.title}>Смена пароля</h2>
        
        <div
          style={{
                ...defaultStyles.error,
                ...(errors.message && defaultStyles.errorVisible)
              }}
            >
            {errors.message}
        </div>

        <form onSubmit={handleSubmit} style={defaultStyles.form}>

            <div style={styles.passwordWrapper}>
                <input
                  type={showPassword ? 'text' : 'password'}
                  placeholder="Пароль"
                  style={{ 
                    ...defaultStyles.input,
                    borderColor: errors.password === false ? '#1e90ff' : 'red',
                  }}
                  value={formData.password}
                  onChange={(e) => handleInputChange('password', e.target.value)}
                />
                <button
                  type="button"
                  style={styles.eyeButton}
                  onClick={() => setShowPassword(!showPassword)}
                  aria-label={showPassword ? 'Скрыть пароль' : 'Показать пароль'}
                >
                <svg
                  style={styles.eyeIcon}
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  {showPassword ? (
                    <>
                      <path d="M12 6a9.77 9.77 0 0 1 8.82 5.5A9.77 9.77 0 0 1 12 17a9.77 9.77 0 0 1-8.82-5.5A9.77 9.77 0 0 1 12 6zm0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5a2.5 2.5 0 0 1 0 5 2.5 2.5 0 0 1 0-5z"/>
                      <path d="M0 0h24v24H0z" fill="none"/>
                    </>
                  ) : (
                    <>
                        <path d="M2 2L22 22" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 14.2362C13.4692 14.7112 12.7684 15.0001 12 15.0001C10.3431 15.0001 9 13.657 9 12.0001C9 11.1764 9.33193 10.4303 9.86932 9.88818" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </>
                  )}
                </svg>
                </button>
            </div>



            <div style={styles.passwordWrapper}>
                <input
                    type={showConfirmPassword ? 'text' : 'password'}
                    placeholder="Повторите пароль"
                    style={{...defaultStyles.input, borderColor: errors.confirmPassword === false ? '#1e90ff' : 'red'}}
                    value={formData.confirmPassword}
                    onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                />

                <button
                    type="button"
                    style={styles.eyeButton}
                    onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                    aria-label={showConfirmPassword ? 'Скрыть пароль' : 'Показать пароль'}
                  >
                <svg
                  style={styles.eyeIcon}
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  {showConfirmPassword ? (
                    <>
                      <path d="M12 6a9.77 9.77 0 0 1 8.82 5.5A9.77 9.77 0 0 1 12 17a9.77 9.77 0 0 1-8.82-5.5A9.77 9.77 0 0 1 12 6zm0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5a2.5 2.5 0 0 1 0 5 2.5 2.5 0 0 1 0-5z"/>
                      <path d="M0 0h24v24H0z" fill="none"/>
                    </>
                  ) : (
                    <>
                        <path d="M2 2L22 22" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M6.71277 6.7226C3.66479 8.79527 2 12 2 12C2 12 5.63636 19 12 19C14.0503 19 15.8174 18.2734 17.2711 17.2884M11 5.05822C11.3254 5.02013 11.6588 5 12 5C18.3636 5 22 12 22 12C22 12 21.3082 13.3317 20 14.8335" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                        <path d="M14 14.2362C13.4692 14.7112 12.7684 15.0001 12 15.0001C10.3431 15.0001 9 13.657 9 12.0001C9 11.1764 9.33193 10.4303 9.86932 9.88818" stroke="#000000" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                    </>
                  )}
                </svg>
                  </button>
          </div>

          <button type="submit" style={defaultStyles.button}>
            Сменить пароль
          </button>
        </form>


        <div style={styles.links}>
          <Link to="/login" style={styles.link}>
            Вернуться назад
          </Link>
        </div>
      </div>
    </div>
  );
};

export default ChangePasswordPage;
