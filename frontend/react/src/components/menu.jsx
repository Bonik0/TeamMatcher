import React, { useEffect, useState } from "react";
import { styles } from "../styles/menu";
import {
	deleteTokens,
	fetchWithTokens,
	getUserInfoByToken,
	goToLoginPage,
} from "../utils/auth";

const SideMenu = () => {
	const [isOpen, setIsOpen] = useState(false);
	const [userData, setUserData] = useState(getUserInfoByToken());

	useEffect(() => {
		const fetchUserData = async () => {
			const userData = getUserInfoByToken();
			setUserData(userData);
		};
		fetchUserData();
	}, []);

	const MainPage = () => {
		window.location.href = "/";
	};

	const logout = async () => {
		await fetchWithTokens(
			"GET",
			"http://localhost:8000/api/auth/token/logout",
		);
		deleteTokens();
		goToLoginPage();
	};

	const fullLogout = async () => {
		await fetchWithTokens(
			"GET",
			"http://localhost:8000/api/auth/token/full-logout",
		);
		deleteTokens();
		goToLoginPage();
	};

	const toggleMenu = () => setIsOpen(!isOpen);

	const userCompetencesPage = () => {
		window.location.href = "/user/competences";
	};
	const teamsPage = () => {
		window.location.href = "/teams";
	};

	const userProjectRolePage = () => {
		window.location.href = "/user/roles";
	};

	const organizerProjectPage = () => {
		window.location.href = "/organizer/projects";
	};

	return (
		<>
			<button
				onClick={toggleMenu}
				style={styles.menuButton}
				aria-label="Открыть меню"
			>
				☰
			</button>

			<div
				style={{
					...styles.menuOverlay,
					opacity: isOpen ? 1 : 0,
					pointerEvents: isOpen ? "all" : "none",
				}}
			>
				<div
					style={{
						...styles.menuContent,
						transform: isOpen ? "translateX(0)" : "translateX(100%)",
					}}
				>
					<nav style={styles.menuNav}>
						<button style={styles.menuItem} onClick={MainPage}>Главная</button>

						{userData.userRole == "user" && (
							<>
								<div style={styles.menuDivider} />
								<button style={styles.menuItem} onClick={userCompetencesPage}>
									Мои компетенции
								</button>
								<div style={styles.menuDivider} />
								<button style={styles.menuItem} onClick={userProjectRolePage}>
									Мои заявки
								</button>
							</>
						)}

						{userData.userRole == "organizer" && (
							<>
								<div style={styles.menuDivider} />
								<button style={styles.menuItem} onClick={organizerProjectPage}>
									Мои проекты
								</button>
							</>
						)}

						<div style={styles.menuDivider} />
						<button style={styles.menuItem} onClick={teamsPage}>Команды</button>

						<div style={styles.menuDivider} />
						<button style={styles.menuItem} onClick={logout}>Выйти</button>
						<div style={styles.menuDivider} />
						<button style={styles.menuItem} onClick={fullLogout}>
							Выйти со всех устройств
						</button>
					</nav>
				</div>
			</div>
		</>
	);
};

export default SideMenu;
