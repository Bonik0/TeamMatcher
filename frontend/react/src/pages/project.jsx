import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { defaultStyles } from "../styles/default";
import { projectPageStyles } from "../styles/projectPage";
import { fetchWithTokens, getUserInfoByToken } from "../utils/auth";

export default function ProjectPage() {
	const { id } = useParams();
	const [project, setProject] = useState(null);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");
	const [expandedRoles, setExpandedRoles] = useState({});
	const [userApplication, setUserApplication] = useState([]);
	const [selectedRoles, setSelectedRoles] = useState([]);

	const user = getUserInfoByToken();
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
				const response = await fetch(
					`http://localhost:8000/api/search/project/${id}`,
				);
				if (!response.ok) {
					setError("Не удалось загрузить проект");
					setLoading(false);
					return;
				}
				const response_dict = await response.json();
				setProject(response_dict);

				if (user.userRole === "user") {
					const roleResponse = await fetchWithTokens(
						"GET",
						`http://localhost:8000/api/user/role/project/${id}`,
					);
					if (roleResponse && roleResponse.ok) {
						const rolesData = await roleResponse.json();
						setUserApplication(rolesData.roles || []);
						setSelectedRoles(rolesData.roles || []);
					} else {
						setUserApplication([]);
						setSelectedRoles([]);
					}
				}
			} catch (e) {
				setError("Ошибка сети");
			} finally {
				setLoading(false);
			}
		};
		load();
	}, [id]);

	const toggleRoleCompetences = (roleId) => {
		setExpandedRoles((prev) => ({ ...prev, [roleId]: !prev[roleId] }));
	};

	const [editMode, setEditMode] = useState(false);

	const isRoleSelected = (project_role_id) =>
		selectedRoles.some((r) =>
			String(r.project_role_id) === String(project_role_id)
		);

	const startNewApplication = () => {
		setSelectedRoles([]);
		setEditMode(true);
	};
	const startEditApplication = () => {
		setSelectedRoles(userApplication.map((role) => ({ ...role })));
		setEditMode(true);
	};
	const cancelEdit = () => {
		setSelectedRoles(userApplication.map((role) => ({ ...role })));
		setEditMode(false);
	};

	const normalizePriorities = (arr) =>
		arr.map((r, i) => ({ ...r, priority: i + 1 }));
	const onDragStart = (e, project_role_id) => {
		e.dataTransfer.setData("text/plain", String(project_role_id));
	};
	const onDragOverSelected = (e) => {
		e.preventDefault();
	};
	const onDropOnSelected = (e, targetId) => {
		e.preventDefault();
		const dragged = e.dataTransfer.getData("text/plain");
		if (!dragged) {
			return;
		}
		if (String(dragged) === String(targetId)) {
			return;
		}
		setSelectedRoles((prev) => {
			const arr = prev.map((r) => ({ ...r }));
			const draggedIdx = arr.findIndex((r) =>
				String(r.project_role_id) === String(dragged)
			);
			const targetIdx = arr.findIndex((r) =>
				String(r.project_role_id) === String(targetId)
			);
			if (draggedIdx === -1 || targetIdx === -1) {
				return arr;
			}
			const [item] = arr.splice(draggedIdx, 1);
			arr.splice(targetIdx, 0, item);
			return normalizePriorities(arr);
		});
	};
	const onDropOnSelectedEnd = (e) => {
		e.preventDefault();
		const dragged = e.dataTransfer.getData("text/plain");
		if (!dragged) {
			return;
		}
		setSelectedRoles((prev) => {
			const arr = prev.map((r) => ({ ...r }));
			const draggedIdx = arr.findIndex((r) =>
				String(r.project_role_id) === String(dragged)
			);
			if (draggedIdx === -1) {
				return arr;
			}
			const [item] = arr.splice(draggedIdx, 1);
			arr.push(item);
			return normalizePriorities(arr);
		});
	};

	const submitApplication = async () => {
		try {
			const normalized = normalizePriorities(selectedRoles.slice());
			const body = JSON.stringify({
				project_id: Number(id),
				roles: normalized.map((r) => ({
					project_role_id: Number(r.project_role_id),
					priority: Number(r.priority),
				})),
			});
			const response = await fetchWithTokens(
				"PUT",
				"http://localhost:8000/api/user/role",
				body,
			);
			if (!response.ok) {
				setError("Не удалось отправить заявку");
				return;
			}
			setUserApplication(normalizePriorities(selectedRoles.slice()));
			setEditMode(false);
		} catch (e) {
			setError("Ошибка сети");
		}
	};

	const deleteApplication = async () => {
		try {
			const body = JSON.stringify({ project_id: Number(id) });
			const response = await fetchWithTokens(
				"DELETE",
				"http://localhost:8000/api/user/role",
				body,
			);
			if (!response.ok) {
				setError("Не удалось удалить заявку");
				return;
			}
			setUserApplication([]);
			setSelectedRoles([]);
		} catch (e) {
			setError("Ошибка сети");
		}
	};

	const cancelProjectOrganizer = async () => {
		try {
			const body = JSON.stringify({ project_id: Number(id) });
			const response = await fetchWithTokens(
				"POST",
				"http://localhost:8000/api/project/cancel",
				body,
			);
			if (!response.ok) {
				setError("Не удалось отменить проект");
				return;
			}
			const resp = await fetch(
				`http://localhost:8000/api/search/project/${id}`,
			);
			if (resp.ok) {
				const response_dict = await resp.json();
				setProject(response_dict);
			}
		} catch (e) {
			setError("Ошибка сети");
		}
	};

	const formTeamsOrganizer = async () => {
		try {
			const body = JSON.stringify({ project_id: Number(id) });
			const response = await fetchWithTokens(
				"POST",
				"http://localhost:8000/api/project/match",
				body,
			);
			if (!response.ok) {
				setError("Не удалось сформировать команды");
				return;
			}
			const resp = await fetch(
				`http://localhost:8000/api/search/project/${id}`,
			);
			if (resp.ok) {
				const response_dict = await resp.json();
				setProject(response_dict);
			}
		} catch (e) {
			setError("Ошибка сети");
		}
	};

	if (loading) {
		return (
			<div style={defaultStyles.container}>
				<div style={defaultStyles.card}>
					<div style={defaultStyles.loading}>
						Загрузка...
					</div>
				</div>
			</div>
		);
	}
	if (error) {
		return (
			<div style={defaultStyles.container}>
				<div style={defaultStyles.card}>
					<div style={defaultStyles.noText}>
						{error}
					</div>
				</div>
			</div>
		);
	}
	if (!project) {
		return null;
	}

	const roles = project.roles || [];

	return (
		<div style={defaultStyles.container}>
			<div style={{ ...defaultStyles.itemsContainer, maxWidth: 900 }}>
				<div style={projectPageStyles.card}>
					<div style={projectPageStyles.header}>
						<h1 style={projectPageStyles.title}>{project.name}</h1>
						<div style={projectPageStyles.meta}>
							<div
								style={{
									...projectPageStyles.statusBadge,
									background: project.status === "recruiting"
										? "#e6f7ff"
										: project.status === "cancelled"
										? "#ffe6e6"
										: "#f0f8e6",
									color: project.status === "cancelled" ? "#b30000" : "#333",
								}}
							>
								{projectStatusMapping[project.status]}
							</div>
							<div style={projectPageStyles.countTitle}>
								{project.user_forms_count} участников
							</div>
						</div>
					</div>
					<div style={projectPageStyles.description}>
						{project.description}
						{project.status === "recruiting" && project.start_time && (
							<div style={{ marginTop: 8 }}>
								Время начала: {new Date(project.start_time).toLocaleString()}
							</div>
						)}
					</div>

					<div style={projectPageStyles.rolesList}>
						{roles.map((role) => (
							<div key={role.id} style={projectPageStyles.roleRow}>
								<div style={projectPageStyles.roleHeader}>
									<div
										onClick={() =>
											toggleRoleCompetences(role.id)}
										style={projectPageStyles.roleName}
									>
										{role.role.name}
									</div>
									<div style={projectPageStyles.roleQuantity}>
										x {role.quantity_per_team}
									</div>
								</div>

								<div style={projectPageStyles.roleDescription}>
									{role.description}
								</div>
								{expandedRoles[role.id] && (
									<div style={projectPageStyles.competencesList}>
										{(role.competences || []).map((comp) => (
											<div
												key={comp.competence.id}
												style={projectPageStyles.competenceChip}
											>
												{comp.competence.name}
											</div>
										))}
									</div>
								)}
							</div>
						))}
					</div>

					{user.userRole === "organizer" && project.status === "recruiting" &&
						String(project.organizer_id) === String(user.userId) && (
						<div
							style={{
								marginTop: 24,
								display: "flex",
								justifyContent: "center",
								gap: "1rem",
							}}
						>
							<button
								style={projectPageStyles.buttonDanger}
								onClick={cancelProjectOrganizer}
							>
								Отменить
							</button>
							<button
								style={projectPageStyles.button}
								onClick={formTeamsOrganizer}
							>
								Сформировать
							</button>
						</div>
					)}
					{user.userRole === "user" &&
						(project.status === "recruiting" || userApplication.length > 0) && (
						<div style={{ marginTop: 40 }}>
							<h3 style={projectPageStyles.applicationName}>Моя заявка</h3>

							{userApplication.length === 0 && !editMode && (
								<div
									style={{
										alignItems: "center",
										display: "flex",
										justifyContent: "center",
									}}
								>
									<button
										style={projectPageStyles.startButton}
										onClick={startNewApplication}
									>
										Подать заявку
									</button>
								</div>
							)}

							{userApplication.length > 0 && !editMode && (
								<div>
									<div
										style={{
											display: "flex",
											flexDirection: "column",
											gap: "0.5rem",
											marginBottom: "1.5rem",
											marginTop: "1.5rem",
										}}
									>
										{userApplication.slice().sort((a, b) =>
											a.priority - b.priority
										).map((project_role) => {
											const roleObj = roles.find((role) =>
												String(role.id) === String(project_role.project_role_id)
											);
											const name = roleObj.role.name;
											return (
												<div
													key={project_role.project_role_id}
													style={{
														...projectPageStyles.competenceChip,
														display: "flex",
														justifyContent: "space-between",
														alignItems: "center",
													}}
												>
													<div style={projectPageStyles.projectRoleName}>
														{name}
													</div>
													<span style={{ fontSize: "1.2rem" }}>
														#{project_role.priority}
													</span>
												</div>
											);
										})}
									</div>
									{project.status === "recruiting" && (
										<div
											style={{
												alignItems: "center",
												display: "flex",
												justifyContent: "center",
												gap: "1rem",
											}}
										>
											<button
												style={projectPageStyles.button}
												onClick={startEditApplication}
											>
												Изменить
											</button>
											<button
												style={projectPageStyles.buttonDanger}
												onClick={deleteApplication}
											>
												Удалить
											</button>
										</div>
									)}
								</div>
							)}

							{editMode && (
								<div>
									<div
										style={{
											marginTop: "1.5rem",
											alignItems: "center",
											justifyContent: "center",
											gap: "1rem",
										}}
									>
										{selectedRoles.length > 0 && (
											<div style={{ fontSize: "1.4rem", textAlign: "center" }}>
												Выбранные роли (переместите для установки приоритета)
											</div>
										)}

										{selectedRoles.length > 0 && (
											<div
												onDragOver={onDragOverSelected}
												onDrop={onDropOnSelectedEnd}
												style={{
													display: "flex",
													flexDirection: "column",
													gap: "0.5rem",
													marginBottom: "1.5rem",
													marginTop: "1.5rem",
												}}
											>
												{selectedRoles
													.slice()
													.sort((a, b) => a.priority - b.priority)
													.map((sel) => {
														const roleObj = roles.find((role) =>
															String(role.id) === String(sel.project_role_id)
														);
														const name = roleObj
															? roleObj.role.name
															: sel.project_role_id;
														return (
															<div
																key={sel.project_role_id}
																draggable
																onDragStart={(e) =>
																	onDragStart(e, sel.project_role_id)}
																onDragOver={(e) => onDragOverSelected(e)}
																onDrop={(e) =>
																	onDropOnSelected(e, sel.project_role_id)}
																style={{
																	...projectPageStyles.competenceChip,
																	display: "flex",
																	justifyContent: "space-between",
																	alignItems: "center",
																}}
															>
																<div
																	style={{
																		display: "flex",
																		alignItems: "center",
																		gap: "0.5rem",
																	}}
																>
																	<div
																		style={projectPageStyles.projectRoleName}
																	>
																		{name}
																	</div>
																</div>
																<div>
																	<button
																		type="button"
																		onClick={() => {
																			setSelectedRoles((prev) =>
																				normalizePriorities(prev.filter((r) =>
																					String(r.project_role_id) !==
																						String(sel.project_role_id)
																				))
																			);
																		}}
																		style={{
																			marginLeft: 6,
																			background: "transparent",
																			border: "none",
																			cursor: "pointer",
																			color: "#1e90ff",
																		}}
																	>
																		×
																	</button>
																</div>
															</div>
														);
													})}
											</div>
										)}
									</div>

									<div style={{ marginTop: 12 }}>
										<div
											style={{
												display: "flex",
												flexDirection: "column",
												gap: "0.5rem",
												marginBottom: "1.5rem",
												marginTop: "1.5rem",
											}}
										>
											{roles.filter((role) =>
														!isRoleSelected(role.id)
													).length > 0 && (
												<div
													style={{ fontSize: "1.4rem", textAlign: "center" }}
												>
													Доступные роли
												</div>
											)}
											{roles
												.filter((role) => !isRoleSelected(role.id))
												.map((role) => (
													<div
														key={role.id}
														onClick={() => {
															setSelectedRoles((prev) =>
																normalizePriorities([...prev, {
																	project_role_id: role.id,
																	priority: prev.length + 1,
																}])
															);
														}}
														style={{
															...projectPageStyles.competenceChip,
															display: "flex",
															justifyContent: "space-between",
															alignItems: "center",
														}}
													>
														<span style={projectPageStyles.projectRoleName}>
															{role.role.name}
														</span>
														<span style={projectPageStyles.roleQuantity}>
															x {role.quantity_per_team}
														</span>
													</div>
												))}
										</div>
									</div>

									<div
										style={{
											marginTop: 8,
											alignItems: "center",
											display: "flex",
											justifyContent: "center",
											gap: "1rem",
										}}
									>
										<button
											style={projectPageStyles.button}
											onClick={submitApplication}
										>
											Сохранить
										</button>
										<button
											style={projectPageStyles.buttonDanger}
											onClick={cancelEdit}
										>
											Отмена
										</button>
									</div>
								</div>
							)}
						</div>
					)}
				</div>
			</div>
		</div>
	);
}
