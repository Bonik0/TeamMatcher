import React, { useEffect, useState } from "react";
import { defaultStyles } from "../styles/default";
import { getEmailVerifyParams, setParamsAndRedirect } from "../utils/auth";
import { styles } from "../styles/emailValidation";

const EmailVerificationPage = () => {
	const NEXT_EMAIL_TIMEOUT = 60;
	const [defaultEmail, redirect_url] = getEmailVerifyParams();

	const [step, setStep] = useState("email");
	const [email, setEmail] = useState(defaultEmail);
	const [code, setCode] = useState(["", "", "", "", "", ""]);
	const [opId, setOpId] = useState("");
	const [error, setError] = useState("");
	const [timer, setTimer] = useState(0);
	const [isTimerActive, setIsTimerActive] = useState(false);

	useEffect(() => {
		let interval;
		if (isTimerActive && timer > 0) {
			interval = setInterval(
				() => {
					setTimer((prev) => prev - 1);
				},
				1000,
			);
		}
		return () => clearInterval(interval);
	}, [isTimerActive, timer]);

	const startTimer = (seconds) => {
		setTimer(seconds);
		setIsTimerActive(true);
	};

	const formatTime = (seconds) => {
		const mins = Math.floor(seconds / 60).toString().padStart(2, "0");
		const secs = (seconds % 60).toString().padStart(2, "0");
		return `${mins}:${secs}`;
	};

	const setEmailChange = (email) => {
		setError("");
		setEmail(email);
	};

	const handleEmailSubmit = async (e) => {
		e.preventDefault();

		if (!email.includes("@")) {
			setError("Введите корректный email");
			return;
		}

		const response = await fetch(`http://localhost:8000/api/email/code/send`, {
			method: "POST",
			headers: {
				"Content-Type": "application/json",
			},
			body: JSON.stringify({ email: email }),
		});

		if (response.status === 422) {
			setError("Введите корректный email");
			return;
		}

		const response_dict = await response.json();

		if (response.status === 429) {
			startTimer(response_dict["block_time"]);
			setError(
				`Вы не можете сейчас получить письмо. Попробуйте через ${
					response_dict["block_time"]
				} секунд`,
			);
			return;
		}

		if (response.status === 200) {
			startTimer(NEXT_EMAIL_TIMEOUT);
			setOpId(response_dict["operation_id"]);
			setStep("code");
			setError("");
		}
	};

	const handleCodeChange = (index, value) => {
		const newCode = [...code];
		const numericValue = value.replace(/\D/g, "");
		newCode[index] = numericValue.slice(-1);
		setCode(newCode);
		setError("");

		if (numericValue && index < 5) {
			document.getElementById(`code-input-${index + 1}`).focus();
		}
	};

	const handleKeyDown = (index, e) => {
		if (e.key === "Backspace") {
			setError("");
			if (!code[index] && index > 0) {
				const newCode = [...code];
				newCode[index - 1] = "";
				setCode(newCode);
				document.getElementById(`code-input-${index - 1}`).focus();
			}
		}
	};

	const handleResendCode = async () => {
		const response = await fetch(`http://localhost:8000/api/email/code/send`, {
			method: "POST",
			headers: { "Content-Type": "application/json" },
			body: JSON.stringify({ email: email }),
		});

		const response_dict = await response.json();

		if (response.status == 429) {
			startTimer(response_dict["block_time"]);
		}

		if (response.status === 200) {
			startTimer(NEXT_EMAIL_TIMEOUT);
			setOpId(response_dict["operation_id"]);
			setError("");
		}
	};

	const handleCodeSubmit = async (e) => {
		e.preventDefault();
		const sended_code = code.join("");

		if (sended_code.length !== 6) {
			setError("Введите код полностью");
			return;
		}
		const response = await fetch(
			`http://localhost:8000/api/email/code/verify`,
			{
				method: "POST",
				headers: { "Content-Type": "application/json" },
				body: JSON.stringify({
					code: sended_code,
					email: email,
					operation_id: opId,
				}),
			},
		);

		const response_dict = await response.json();

		if (response.status === 400) {
			setError("Повторно отправте код");
			return;
		}

		if (response.status === 200) {
			if (response_dict["is_correct_code"] === false) {
				setError("Неверный код");
				return;
			}
			setParamsAndRedirect(redirect_url, opId, email);
		}
	};

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.card}>
				<h2 style={defaultStyles.title}>
					{step === "email" ? "Подтверждение почты" : "Введите код"}
				</h2>

				<div
					style={{
						...defaultStyles.error,
						...(error && defaultStyles.errorVisible),
					}}
				>
					{error}
				</div>

				{step === "email"
					? (
						<form onSubmit={handleEmailSubmit} style={defaultStyles.form}>
							<input
								type="email"
								placeholder="Введите вашу почту"
								style={{
									...defaultStyles.input,
									borderColor: error === "" ? "#1e90ff" : "red",
								}}
								value={email}
								onChange={(e) => setEmailChange(e.target.value)}
							/>
							<button type="submit" style={defaultStyles.button}>
								Отправить код подтверждения
							</button>
						</form>
					)
					: (
						<div style={styles.codeContainer}>
							<div style={styles.codeInputs}>
								{code.map((digit, index) => (
									<input
										key={index}
										id={`code-input-${index}`}
										type="text"
										inputMode="numeric"
										maxLength="1"
										autoComplete="one-time-code"
										style={{
											...styles.codeInput,
											borderColor: error === "" ? "#1e90ff" : "red",
										}}
										value={digit}
										onChange={(e) => handleCodeChange(index, e.target.value)}
										onKeyDown={(e) => handleKeyDown(index, e)}
										onFocus={(e) => e.target.select()}
									/>
								))}
							</div>

							<button
								type="button"
								style={{
									...styles.resendButton,
									...(timer > 0 ? styles.resendDisabled : {}),
								}}
								onClick={handleResendCode}
								disabled={timer > 0}
							>
								{timer > 0
									? `Запросить новый код через ${formatTime(timer)}`
									: "Отправить код повторно"}
							</button>

							<button
								type="submit"
								style={defaultStyles.button}
								onClick={handleCodeSubmit}
							>
								Подтвердить
							</button>
						</div>
					)}
			</div>
		</div>
	);
};

export default EmailVerificationPage;
