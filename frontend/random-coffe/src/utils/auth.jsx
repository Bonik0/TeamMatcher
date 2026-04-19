


function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}


  
export const refreshTokens = async () => {
    const refreshToken = localStorage.getItem('refresh_token');
    var exp = localStorage.getItem('exp');

    if (!refreshToken || !exp) {
      return false;
    }
    exp = parseInt(exp);
    
    if (Date.now() / 1000 < exp - 60) {
        return true;
    };
    const isUpdate = localStorage.getItem('is_update');

    if (isUpdate === '') {
        do {
            await sleep(100);
        } while (localStorage.getItem('is_update') === '');
        return true;
    };

    localStorage.setItem('is_update', '');
    
  
    const response = await fetch('http://localhost:8000/api/auth/token/update', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({refresh_token : refreshToken})
    });

    const response_dict = await response.json();

    if (response.status === 200) {
        setTokens(response_dict);
        localStorage.removeItem('is_update');
        return true;
    };

    localStorage.removeItem('is_update');
    return false;
};
  
  
export const setTokens = (response_dict) => {
    localStorage.setItem('access_token', response_dict['access_token']);
    localStorage.setItem('refresh_token', response_dict['refresh_token']);
    localStorage.setItem('exp', response_dict['exp']);
};

export const deleteTokens = () => {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
    localStorage.removeItem('exp');
}; 


export const fetchWithTokens = async (method, url, body = null) => {

    if (await refreshTokens()) {
        const accessToken = localStorage.getItem('access_token');
        const response = await fetch(url, {
            method: method,
            headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${accessToken}`
                },
            body: body
          });
        return response;
    };
    goToLoginPage();
    return null;
};



export const getURLtoEmailVetify = (redirect_url, email = null) => {
    if (!email){
        return `/email-verify?redirect_url=${redirect_url}`
    }
    return `/email-verify?redirect_url=${redirect_url}&email=${email}`
};

export const getEmailVerifyParams = () => {
    const params = new URL(document.location.toString()).searchParams;
    const redirect_url = params.get('redirect_url');
    const email = params.get('email') || '';
    if (!redirect_url){
      goToLoginPage();
    }
    return [email, redirect_url];
};


export const setParamsAndRedirect = (redirect_url, opId, email) => {
    window.location.href = `${redirect_url}?op_id=${opId}&email=${email}`
};


export const goToLoginPage = () => {
    window.location.href = '/login';
}



export const getAuthParams = () => {
    const params = new URL(document.location.toString()).searchParams;
    const opId = params.get('op_id');
    const email = params.get('email');
    if (!opId || !email){
        window.location.href = getURLtoEmailVetify(window.location.pathname, email);
    };
    return [opId, email];
};