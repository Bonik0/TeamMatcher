import React, { useEffect, useState } from "react";
import { defaultStyles } from "../styles/default";
import { organizerProjectsStyles } from "../styles/organizerProjects";
import { fetchWithTokens } from "../utils/auth";
import { useNavigate } from "react-router-dom";
import { projectPageStyles } from "../styles/projectPage";

export default function OrganizerProjectsPage() {
	const [projects, setProjects] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");
	const navigate = useNavigate();
	const projectStatusMapping = {
		recruiting: "Запланирован",
		cancelled: "Отменен",
		completed: "Завершен",
		formated: "Формирование",
	};

	useEffect(() => {
		const load = async () => {
			setLoading(true);
			setError("");
			try {
				const url = "http://localhost:8000/api/project/";
				const response = await fetchWithTokens("GET", url);
				if (!response.ok) {
					setError("Не удалось загрузить проекты");
					setProjects([]);
					setLoading(false);
					return;
				}
				const response_dict = await response.json();
				setProjects(response_dict.projects);
			} catch (e) {
				setError("Ошибка сети");
			} finally {
				setLoading(false);
			}
		};
		load();
	}, []);

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					<div style={{ textAlign: "center" }}>
						<h2 style={defaultStyles.title}>Мои проекты</h2>
					</div>
					<div
						style={{
							display: "flex",
							justifyContent: "flex-end",
							marginTop: "0.5rem",
						}}
					>
						<button
							style={{ ...defaultStyles.button, padding: "0.6rem 1rem" }}
							onClick={() => navigate("/project/create")}
						>
							Создать
						</button>
					</div>

					{loading && <div style={defaultStyles.loading}>Загрузка...</div>}
					{error && (
						<div style={{ ...defaultStyles.noText, color: "red" }}>{error}</div>
					)}

					<div
						style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
					>
						{!loading && !error && projects.length === 0 && (
							<div style={defaultStyles.noText}>Нет проектов</div>
						)}

						{projects.map((project) => (
							<div key={project.id}>
								<div
									style={organizerProjectsStyles.projectCard}
									onMouseEnter={(e) => {
										e.currentTarget.style.boxShadow =
											"0 4px 12px rgba(0,0,0,0.06)";
									}}
									onMouseLeave={(e) => {
										e.currentTarget.style.boxShadow = "none";
									}}
								>
									<div style={organizerProjectsStyles.projectHeader}>
										<h2
											style={{
												...organizerProjectsStyles.projectTitle,
												cursor: "pointer",
												margin: 0,
											}}
											onClick={(e) => {
												e.stopPropagation();
												navigate(`/project/${project.id}`);
											}}
										>
											{project.name}
										</h2>

										<div
											style={{
												...projectPageStyles.statusBadge,
												marginLeft: "auto",
												display: "inline-block",
												marginTop: "0.5rem",
												whiteSpace: "nowrap",
												background: project.status === "recruiting"
													? "#e6f7ff"
													: project.status === "cancelled"
													? "#ffe6e6"
													: "#f0f8e6",
												color: project.status === "cancelled"
													? "#b30000"
													: "#333",
											}}
										>
											{projectStatusMapping[project.status]}
										</div>
									</div>
									<p style={organizerProjectsStyles.projectDescription}>
										{project.description}
									</p>
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	);
}
