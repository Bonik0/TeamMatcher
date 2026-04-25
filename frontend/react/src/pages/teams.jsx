import React, { useEffect, useState } from "react";
import { defaultStyles } from "../styles/default";
import { teamsStyles } from "../styles/teams";
import { fetchWithTokens, getUserInfoByToken } from "../utils/auth";
import { useNavigate } from "react-router-dom";

export default function TeamsPage() {
	const [projects, setProjects] = useState([]);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");
	const [expanded, setExpanded] = useState({});
	const navigate = useNavigate();
	const user = getUserInfoByToken();

	useEffect(() => {
		const load = async () => {
			setLoading(true);
			setError("");
			try {
				let url = "";
				if (user.userRole === "organizer") {
					url = "http://localhost:8000/api/project/teams";
				} else {
					url = "http://localhost:8000/api/user/team";
				}
				const response = await fetchWithTokens("GET", url);
				if (!response.ok) {
					setError("Не удалось загрузить проекты");
					setProjects([]);
					setLoading(false);
					return;
				}
				const response_dict = await response.json();
				setProjects(response_dict.projects || []);
			} catch (e) {
				setError("Ошибка сети");
			} finally {
				setLoading(false);
			}
		};
		load();
	}, []);

	const toggleProject = (id) => {
		setExpanded((prev) => ({ ...prev, [id]: !prev[id] }));
	};

	const getRoleNameById = (project, project_role_id) => {
		const role = (project.roles || []).find((r) =>
			String(r.id) === String(project_role_id)
		);
		return role?.role?.name ?? "роль";
	};

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					<h2 style={defaultStyles.title}>Команды</h2>

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
									onClick={() => toggleProject(project.id)}
									style={teamsStyles.projectCard}
									onMouseEnter={(e) => {
										e.currentTarget.style.boxShadow =
											"0 4px 12px rgba(0,0,0,0.06)";
									}}
									onMouseLeave={(e) => {
										e.currentTarget.style.boxShadow = "none";
									}}
								>
									<h2
										style={{ ...teamsStyles.projectTitle, cursor: "pointer" }}
										onClick={(e) => {
											e.stopPropagation();
											navigate(`/project/${project.id}`);
										}}
									>
										{project.name}
									</h2>
									<p style={teamsStyles.projectDescription}>
										{project.description}
									</p>
									{expanded[project.id] && (
										<div style={teamsStyles.teamsContainer}>
											{(project.teams || []).map((team) => (
												<div key={team.id} style={teamsStyles.teamCard}>
													<h2 style={teamsStyles.teamTitle}>{team.name}</h2>
													<div>
														{(team.members || []).map((member) => (
															<div
																key={member.id}
																style={teamsStyles.memberRow}
															>
																<div style={teamsStyles.memberName}>
																	{member.user.first_name} {member.user.surname}
																	{" "}
																	{member.user.patronymic
																		? member.user.patronymic
																		: ""}
																</div>
																<div style={teamsStyles.memberRole}>
																	{getRoleNameById(
																		project,
																		member.project_role_id,
																	)}
																</div>
															</div>
														))}
													</div>
												</div>
											))}
										</div>
									)}
								</div>
							</div>
						))}
					</div>
				</div>
			</div>
		</div>
	);
}
