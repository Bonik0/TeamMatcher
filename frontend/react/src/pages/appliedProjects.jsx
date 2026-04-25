import React, { useEffect, useState } from "react";
import { defaultStyles } from "../styles/default";
import { appliedProjectsStyles } from "../styles/appliedProjects";
import { fetchWithTokens, getUserInfoByToken } from "../utils/auth";
import { useNavigate } from "react-router-dom";

export default function AppliedProjectsPage() {
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
				const url = "http://localhost:8000/api/user/role";
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

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					<h2 style={defaultStyles.title}>Заявки на проекты</h2>

					{loading && <div style={defaultStyles.loading}>Загрузка...</div>}
					{error && (
						<div style={{ ...defaultStyles.noText, color: "red" }}>{error}</div>
					)}

					<div
						style={{ display: "flex", flexDirection: "column", gap: "1rem" }}
					>
						{!error && !loading && projects.length === 0 && (
							<div style={defaultStyles.noText}>Нет заявок</div>
						)}

						{projects.map((project) => (
							<div key={project.id}>
								<div
									onClick={() => toggleProject(project.id)}
									style={appliedProjectsStyles.projectCard}
									onMouseEnter={(e) => {
										e.currentTarget.style.boxShadow =
											"0 4px 12px rgba(0,0,0,0.06)";
									}}
									onMouseLeave={(e) => {
										e.currentTarget.style.boxShadow = "none";
									}}
								>
									<h2
										style={{
											...appliedProjectsStyles.projectTitle,
											cursor: "pointer",
										}}
										onClick={(e) => {
											e.stopPropagation();
											navigate(`/project/${project.id}`);
										}}
									>
										{project.name}
									</h2>
									<p style={appliedProjectsStyles.projectDescription}>
										{project.description}
									</p>
									{expanded[project.id] && (
										<div style={appliedProjectsStyles.rolesContainer}>
											{(() => {
												const applied = project.roles
													.flatMap((role) =>
														role.forms.map((form) => ({
															roleName: role.role.name,
															priority: form.priority,
															project_role_id: role.id,
														}))
													)
													.sort((a, b) =>
														a.priority - b.priority
													);

												if (applied.length === 0) {
													return (
														<div style={appliedProjectsStyles.noRolesText}>
															Вы не подавались на роли в этом проекте
														</div>
													);
												}

												return applied.map((item, idx) => (
													<div
														key={`${project.id}-${item.project_role_id}-${idx}`}
														style={appliedProjectsStyles.roleCard}
													>
														<div style={appliedProjectsStyles.roleName}>
															{item.roleName}
														</div>
														<div style={appliedProjectsStyles.rolePriority}>
															#{item.priority}
														</div>
													</div>
												));
											})()}
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
