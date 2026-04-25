function sleep(ms) {
	return new Promise((resolve) => setTimeout(resolve, ms));
}

export const refreshTokens = async () => {
	const refreshToken = localStorage.getItem("refresh_token");
	const exp = localStorage.getItem("exp");
	const isUpdate = localStorage.getItem("is_update");
	let retryCount = 0;

	if (!refreshToken || !exp) {
		return false;
	}

	if (Date.now() / 1000 < exp - 60) {
		return true;
	}

	if (isUpdate === "") {
		do {
			await sleep(100);
			retryCount += 1;
		} while (localStorage.getItem("is_update") === "" && retryCount < 10);

		if (localStorage.getItem("is_update") === null) {
			return true;
		}
	}

	localStorage.setItem("is_update", "");

	const response = await fetch(`http://localhost:8000/api/auth/token/update`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
		},
		body: JSON.stringify({ refresh_token: refreshToken }),
	});

	const response_dict = await response.json();

	if (response.status === 200) {
		setTokens(response_dict);
		localStorage.removeItem("is_update");
		return true;
	}

	localStorage.removeItem("is_update");
	return false;
};

export const getUserInfoByToken = () => {
	const token = localStorage.getItem("access_token");
	if (token) {
		const payload = JSON.parse(atob(token.split(".")[1]));
		return {
			userId: payload.user_id || "",
			userRole: payload.role || "user",
		};
	}
	return {
		userId: "",
		userRole: "user",
	};
};

export const setTokens = (response_dict) => {
	localStorage.setItem("access_token", response_dict["access_token"]);
	localStorage.setItem("refresh_token", response_dict["refresh_token"]);
	localStorage.setItem(
		"exp",
		Date.now() / 1000 + parseInt(response_dict["exp"]),
	);
};

export const deleteTokens = () => {
	localStorage.removeItem("access_token");
	localStorage.removeItem("refresh_token");
	localStorage.removeItem("exp");
};

export const fetchWithTokens = async (method, url, body = null) => {
	if (await refreshTokens()) {
		const accessToken = localStorage.getItem("access_token");
		const response = await fetch(url, {
			method: method,
			headers: {
				"Content-Type": "application/json",
				"Authorization": `Bearer ${accessToken}`,
			},
			body: body,
		});
		return response;
	}
	goToLoginPage();
	return null;
};

export const getURLtoEmailVetify = (redirect_url, email = null) => {
	if (!email) {
		return `/email-verify?redirect_url=${redirect_url}`;
	}
	return `/email-verify?redirect_url=${redirect_url}&email=${email}`;
};

export const getEmailVerifyParams = () => {
	const params = new URL(document.location.toString()).searchParams;
	const redirect_url = params.get("redirect_url");
	const email = params.get("email") || "";
	if (!redirect_url) {
		goToLoginPage();
	}
	return [email, redirect_url];
};

export const setParamsAndRedirect = (redirect_url, opId, email) => {
	window.location.href = `${redirect_url}?op_id=${opId}&email=${email}`;
};

export const goToLoginPage = () => {
	window.location.href = "/login";
};

export const goToHomePage = () => {
	window.location.href = "/";
};

export const getAuthParams = () => {
	const params = new URL(document.location.toString()).searchParams;
	const opId = params.get("op_id");
	const email = params.get("email");
	if (!opId || !email) {
		window.location.href = getURLtoEmailVetify(window.location.pathname, email);
	}
	return [opId, email];
};
