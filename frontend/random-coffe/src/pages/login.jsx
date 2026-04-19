import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import { styles } from '../styles/auth';
import { defaultStyles } from '../styles/default';
import { setTokens, getURLtoEmailVetify } from '../utils/auth';


const LoginPage = () => {
    const [formData, setFormData] = useState({
        email: '',
        password: '',
      });

    const noErrorsState = {
        email: false,
        password: false,
        message: '',
    }
    const [errors, setErrors] = useState(noErrorsState);
    const [showPassword, setShowPassword] = useState(false);

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

        if (!formData.email.includes('@')) {
            handleErrorsChange('Введите корректный email', 'email');
            return;
        }

        if (formData.password.length < 5) {
            handleErrorsChange('Пароль должен содержать минимум 5 символов', 'password');
            return;
        }

        const response = await fetch('http://localhost:8000/api/auth/login', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email : formData.email, password : formData.password }),
        });

        const response_dict = await response.json();

        if (response.status === 422){
            handleErrorsChange('Введите корректный email', 'email');
            return;
        }

        if (response.status === 400){
            const type = response_dict["detail"]["type"];
            if (type === "invalid_email"){
                handleErrorsChange('Этот email не зарегистрирован', 'email');
            }
            if (type === "invalid_password"){
                handleErrorsChange('Неправильный пароль', 'password');
            }
            if (type === "attempt_count_exceeded"){
                handleErrorsChange(`Превышенно количесво попыток. Попробуйте через ${response_dict["detail"]["remaining_seconds"]} c`, 'password');
            }
            return;
        }

        if (response.status === 200) {
            setTokens(response_dict);
            window.location.href = '/';
        }
    };

  return (
    <div style={defaultStyles.container}>
      <div style={defaultStyles.card}>
        <h2 style={defaultStyles.title}>Вход в аккаунт</h2>
        
        <div
          style={{
                ...defaultStyles.error,
                ...(errors.message && defaultStyles.errorVisible)
              }}
            >
            {errors.message}
        </div>

        <form onSubmit={handleSubmit} style={defaultStyles.form}>
          <input
            type="email"
            placeholder="Email"
            style={{...defaultStyles.input, borderColor: errors.email === false ? '#1e90ff' : 'red'}}
            value={formData.email}
            onChange={(e) => handleInputChange('email', e.target.value)}
          />
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

          <button type="submit" style={defaultStyles.button}>
            Войти
          </button>
        </form>

        <div style={styles.links}>
          <Link to={getURLtoEmailVetify("/register", formData.email)} style={styles.link}>
            Создать аккаунт
          </Link>
          <Link to={getURLtoEmailVetify("/forgot-password", formData.email)} style={styles.link}>
            Забыли пароль?
          </Link>
        </div>
      </div>
    </div>
  );
};

export default LoginPage;