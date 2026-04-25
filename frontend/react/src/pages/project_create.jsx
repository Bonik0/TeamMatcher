import React, { useState } from "react";
import SearchSelect from "../components/SearchSelect";
import { defaultStyles } from "../styles/default";
import { createProjectStyles } from "../styles/createProject";
import { userCompetenceStyles } from "../styles/userCompetences";
import { useNavigate } from "react-router-dom";
import { fetchWithTokens } from "../utils/auth";

export default function ProjectCreatePage() {
	const [name, setName] = useState("");
	const [description, setDescription] = useState("");
	const [startTime, setStartTime] = useState("");
	const noErrorsState = {
		noField: false,
		name: false,
		startTime: false,
		message: "",
	};
	const [errors, setErrors] = useState(noErrorsState);
	const [roles, setRoles] = useState([]);
	const [roleFormVisible, setRoleFormVisible] = useState(false);
	const [roleDraft, setRoleDraft] = useState(null);
	const noRoleErrorsState = { name: false, competences: false, message: "" };
	const [roleErrors, setRoleErrors] = useState(noRoleErrorsState);
	const navigate = useNavigate();

	const handleInputChange = (field, value) => {
		if (field === "name") {
			setName(value);
		}
		if (field === "description") {
			setDescription(value);
		}
		if (field === "startTime") {
			setStartTime(value);
		}
		if (errors[field]) {
			setErrors(noErrorsState);
		}
	};

	const handleErrorsChange = (message, fieldError) => {
		setErrors({
			...noErrorsState,
			[fieldError]: true,
			message: message,
		});
	};

	const validate = () => {
		if (!name || !name.trim()) {
			handleErrorsChange("Необходимо заполнить поле", "name");
			return false;
		}
		if (!startTime) {
			handleErrorsChange("Необходимо заполнить поле", "startTime");
			return false;
		}
		const startDate = new Date(startTime);
		if (isNaN(startDate.getTime()) || startDate.getTime() <= Date.now()) {
			handleErrorsChange("Время старта должно быть в будущем", "startTime");
			return false;
		}
		setErrors(noErrorsState);
		return true;
	};

	const handleCreate = (e) => {
		e.preventDefault();
		if (!validate()) {
			return;
		}
		if (!roles || roles.length === 0) {
			handleErrorsChange("Добавьте хотя бы одну роль", "noField");
			return;
		}
		(async () => {
			try {
				const bodyObj = {
					name: name.trim(),
					description: description || null,
					start_time: new Date(startTime).toISOString(),
					roles: roles.map((role) => ({
						name: role.name,
						description: role.description || null,
						quantity_per_team: Number(role.quantity_per_team),
						competences: role.competences.map((comp) => ({
							name: comp.name,
							importance: Number(comp.importance),
						})),
					})),
				};
				const body = JSON.stringify(bodyObj);
				const url = "http://localhost:8000/api/project/";
				const response = await fetchWithTokens("PUT", url, body);
				if (!response) {
					setErrors({ ...noErrorsState, message: "Неавторизован" });
					return;
				}
				if (!response.ok) {
					setErrors({ ...noErrorsState, message: "Не удалось создать проект" });
					return;
				}
				navigate("/organizer/projects");
			} catch (e) {
				setErrors({ ...noErrorsState, message: "Ошибка сети" });
			}
		})();
	};

	const openRoleForm = () => {
		setRoleDraft({
			name: "",
			quantity: 1,
			description: "",
			competences: [],
			pendingCompetence: null,
			selectedCompetenceSuggestion: null,
			pendingLevel: 1,
			manualCompetenceName: "",
			errors: { name: false, competences: false },
		});
		setRoleFormVisible(true);
	};

	const closeRoleForm = () => {
		setRoleDraft(null);
		setRoleFormVisible(false);
	};

	const handleRoleErrorsChange = (msg, fieldError) => {
		setRoleErrors({
			...noRoleErrorsState,
			[fieldError]: true,
			message: msg,
		});
	};
	const addCompetenceToDraft = () => {
		const nameToAdd = roleDraft?.pendingCompetence?.name ||
			(roleDraft?.manualCompetenceName &&
				roleDraft.manualCompetenceName.trim()) ||
			null;
		if (!nameToAdd) {
			handleRoleErrorsChange("Необходимо заполнить компетенцию", "competences");
			setRoleDraft((prev) => ({
				...prev,
				errors: { ...prev.errors, competences: true },
			}));
			return;
		}
		const exists = (roleDraft.competences || []).some((c) =>
			String(c.name).toLowerCase() === String(nameToAdd).toLowerCase()
		);
		if (exists) {
			handleRoleErrorsChange("Такая компетенция уже добавлена", "competences");
			setRoleDraft((prev) => ({
				...prev,
				errors: { ...prev.errors, competences: true },
			}));
			return;
		}
		const importance = Math.min(10, roleDraft.pendingLevel || 1);
		setRoleDraft((prev) => ({
			...prev,
			competences: [...(prev.competences || []), {
				name: nameToAdd,
				importance,
			}],
			pendingCompetence: null,
			selectedCompetenceSuggestion: null,
			pendingLevel: 1,
			manualCompetenceName: "",
			errors: { ...prev.errors, competences: false },
		}));
		setRoleErrors(noRoleErrorsState);
	};

	const removeCompetenceFromDraft = (idx) => {
		setRoleDraft((prev) => ({
			...prev,
			competences: prev.competences.filter((_, i) => i !== idx),
		}));
	};

	const commitRole = () => {
		if (!roleDraft) return;
		if (!roleDraft.name || !roleDraft.name.trim()) {
			handleRoleErrorsChange("Необходимо заполнить поле", "name");
			setRoleDraft((prev) => ({
				...prev,
				errors: { ...prev.errors, name: true },
			}));
			return;
		}
		if (!roleDraft.quantity || Number(roleDraft.quantity) < 1) {
			handleRoleErrorsChange("Количество участников должно быть >= 1", "name");
			setRoleDraft((prev) => ({
				...prev,
				errors: { ...prev.errors, name: false },
			}));
			return;
		}
		if (!roleDraft.competences || roleDraft.competences.length === 0) {
			handleRoleErrorsChange(
				"Добавьте хотя бы одну компетенцию",
				"competences",
			);
			setRoleDraft((prev) => ({
				...prev,
				errors: { ...prev.errors, competences: true },
			}));
			return;
		}
		setRoles((
			prev,
		) => [...prev, {
			name: roleDraft.name.trim(),
			description: roleDraft.description,
			quantity_per_team: Number(roleDraft.quantity),
			competences: roleDraft.competences,
		}]);
		closeRoleForm();
	};

	const removeRole = (idx) => {
		setRoles((prev) => prev.filter((_, i) => i !== idx));
	};

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					{!roleFormVisible && (
						<h2 style={defaultStyles.title}>Создать проект</h2>
					)}

					{!roleFormVisible && (
						<div
							style={{
								...defaultStyles.error,
								...(errors.message && defaultStyles.errorVisible),
							}}
						>
							{errors.message}
						</div>
					)}

					{!roleFormVisible
						? (
							<form onSubmit={handleCreate}>
								<div style={{ marginBottom: "1rem" }}>
									<input
										placeholder="Название проекта"
										value={name}
										onChange={(e) => handleInputChange("name", e.target.value)}
										style={{
											...defaultStyles.input,
											borderColor: errors.name === false ? "#1e90ff" : "red",
										}}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									<textarea
										placeholder="Описание"
										value={description}
										onChange={(e) =>
											handleInputChange("description", e.target.value)}
										style={{
											...defaultStyles.input,
											height: "6rem",
										}}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									<label style={{ ...defaultStyles.noText }}>
										Время старта:
									</label>
									<input
										type="datetime-local"
										value={startTime}
										onChange={(e) =>
											handleInputChange("startTime", e.target.value)}
										style={{
											...defaultStyles.input,
											marginTop: "0.25rem",
											borderColor: errors.startTime === false
												? "#1e90ff"
												: "red",
										}}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									{roles.length === 0
										? (
											<div style={{ ...defaultStyles.noText }}>
												Роли не добавлены
											</div>
										)
										: (
											<div style={createProjectStyles.rolesContainer}>
												{roles.map((role, i) => (
													<div
														key={i}
														style={createProjectStyles.roleChip}
													>
														<div
															style={{
																display: "flex",
																alignItems: "center",
																gap: "0.5rem",
															}}
														>
															<div style={createProjectStyles.roleName}>
																{role.name}
															</div>
														</div>
														<button
															type="button"
															onClick={() => removeRole(i)}
															style={{
																marginLeft: 6,
																background: "transparent",
																border: "none",
																cursor: "pointer",
																color: "#1e90ff",
															}}
															aria-label="remove-role"
														>
															×
														</button>
													</div>
												))}
											</div>
										)}
								</div>

								<div
									style={{
										marginBottom: "1rem",
										display: "flex",
										justifyContent: "center",
									}}
								>
									<button
										type="button"
										onClick={openRoleForm}
										style={createProjectStyles.createButton}
									>
										Создать роль
									</button>
								</div>

								<div
									style={{
										marginTop: "2rem",
										display: "flex",
										justifyContent: "center",
										gap: "1rem",
									}}
								>
									<button
										type="submit"
										style={createProjectStyles.createButton}
									>
										Создать проект
									</button>
									<button
										type="button"
										onClick={() => navigate(-1)}
										style={createProjectStyles.cancelButton}
									>
										Отмена
									</button>
								</div>
							</form>
						)
						: (
							<div>
								<h2 style={defaultStyles.title}>Создать роль</h2>
								<div
									style={{
										...defaultStyles.error,
										...(roleErrors.message ? defaultStyles.errorVisible : {}),
										marginBottom: "0.5rem",
									}}
								>
									{roleErrors.message}
								</div>
								<div style={{ marginBottom: "1rem" }}>
									<SearchSelect
										placeholder="Название роли"
										fetchUrl="/api/search/role"
										onSelect={(item) =>
											setRoleDraft((prev) => ({
												...prev,
												name: item.name || prev.name,
											}))}
										executedName="roles"
										selectedItems={roles.map((role) => ({ name: role.name }))}
										saveSelected={true}
										inputStyle={roleDraft.errors.name
											? { borderColor: "red" }
											: {}}
										onInputChange={(val) => {
											if (roleDraft.errors.name) {
												setRoleDraft((prev) => ({
													...prev,
													errors: { ...prev.errors, name: false },
												}));
												setRoleErrors(noRoleErrorsState);
											}
										}}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									<input
										type="number"
										min={1}
										placeholder="Количество участников в команде"
										value={roleDraft.quantity}
										onChange={(e) =>
											setRoleDraft((prev) => ({
												...prev,
												quantity: e.target.value,
											}))}
										style={{ ...defaultStyles.input, width: "90px" }}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									<input
										placeholder="Описание роли"
										value={roleDraft.description}
										onChange={(e) =>
											setRoleDraft((prev) => ({
												...prev,
												description: e.target.value,
											}))}
										style={{ ...defaultStyles.input }}
									/>
								</div>

								<div style={{ marginBottom: "1rem" }}>
									<div
										style={{
											display: "flex",
											gap: "0.5rem",
											alignItems: "center",
										}}
									>
										<SearchSelect
											placeholder="Поиск компетенции"
											fetchUrl="/api/search/competence"
											onSelect={(item) =>
												setRoleDraft((prev) => ({
													...prev,
													selectedCompetenceSuggestion: item,
													manualCompetenceName: "",
												}))}
											executedName="competencies"
											selectedItems={roleDraft.competences.map((comp) => ({
												name: comp.name,
											}))}
											saveSelected={true}
											onInputChange={(val) => {
												if (roleDraft.errors.competences) {
													setRoleDraft((prev) => ({
														...prev,
														errors: { ...prev.errors, competences: false },
													}));
												}
												if (roleDraft.pendingCompetence) {
													setRoleDraft((prev) => ({
														...prev,
														pendingCompetence: null,
														pendingLevel: 1,
													}));
												}
												if (
													roleDraft.selectedCompetenceSuggestion && val &&
													val.trim() !==
														roleDraft.selectedCompetenceSuggestion.name
												) {
													setRoleDraft((prev) => ({
														...prev,
														selectedCompetenceSuggestion: null,
													}));
												}
											}}
											inputStyle={roleDraft.errors.competences
												? { borderColor: "red" }
												: {}}
										/>
										<button
											type="button"
											onClick={() => {
												if (roleDraft.selectedCompetenceSuggestion) {
													setRoleDraft((prev) => ({
														...prev,
														pendingCompetence:
															prev.selectedCompetenceSuggestion,
													}));
													return;
												}
												if (
													roleDraft.manualCompetenceName &&
													roleDraft.manualCompetenceName.trim()
												) {
													setRoleDraft((prev) => ({
														...prev,
														pendingCompetence: {
															name: prev.manualCompetenceName.trim(),
														},
														manualCompetenceName: "",
													}));
													return;
												}
												setRoleDraft((prev) => ({
													...prev,
													errors: { ...prev.errors, competences: true },
												}));
											}}
											style={userCompetenceStyles.addConfirmButton}
										>
											✔
										</button>
									</div>

									{(roleDraft?.pendingCompetence) && (
										<div style={{ marginTop: 8 }}>
											<div
												style={{
													marginTop: 8,
													display: "flex",
													gap: "0.4rem",
													flexWrap: "wrap",
													alignItems: "center",
												}}
											>
												{Array.from({ length: 10 }).map((_, idx) => {
													const level = idx + 1;
													return (
														<button
															key={level}
															type="button"
															onClick={() =>
																setRoleDraft((prev) => ({
																	...(prev || {}),
																	pendingLevel: level,
																}))}
															style={{
																...(userCompetenceStyles.levelButton),
																...(roleDraft?.pendingLevel === level
																	? userCompetenceStyles.levelButtonActive
																	: {}),
															}}
														>
															{level}
														</button>
													);
												})}
											</div>

											<div
												style={{
													marginTop: 8,
													display: "flex",
													gap: "0.5rem",
													alignItems: "center",
												}}
											>
												<button
													type="button"
													onClick={addCompetenceToDraft}
													style={userCompetenceStyles.addConfirmButton}
												>
													Добавить
												</button>
												<button
													type="button"
													onClick={() =>
														setRoleDraft((prev) => ({
															...(prev || {}),
															pendingCompetence: null,
															pendingLevel: 1,
														}))}
													style={userCompetenceStyles.addCancelButton}
												>
													Отмена
												</button>
											</div>
										</div>
									)}
								</div>

								<div style={createProjectStyles.rolesContainer}>
									{(roleDraft?.competences || []).map((c, ci) => (
										<div key={ci} style={createProjectStyles.roleChip}>
											<div
												style={{
													display: "flex",
													gap: "0.5rem",
													alignItems: "center",
												}}
											>
												<div style={createProjectStyles.roleName}>{c.name}</div>
												<div style={{ marginLeft: 8, color: "#033b6b" }}>
													({c.importance})
												</div>
											</div>
											<button
												onClick={() =>
													removeCompetenceFromDraft(ci)}
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
									))}
								</div>

								<div
									style={{
										marginTop: "2rem",
										display: "flex",
										justifyContent: "center",
										gap: "1rem",
									}}
								>
									<button
										type="button"
										onClick={commitRole}
										style={{
											backgroundColor: "#1890ff",
											color: "white",
											padding: "0.8rem 1.2rem",
											border: "none",
											borderRadius: 6,
											cursor: "pointer",
											fontSize: "1rem",
											minWidth: "140px",
										}}
									>
										Создать роль
									</button>
									<button
										type="button"
										onClick={closeRoleForm}
										style={{
											backgroundColor: "#ff4d4f",
											color: "white",
											padding: "0.8rem 1.2rem",
											border: "none",
											borderRadius: 6,
											cursor: "pointer",
											fontSize: "1rem",
											minWidth: "140px",
										}}
									>
										Отмена
									</button>
								</div>
							</div>
						)}
				</div>
			</div>
		</div>
	);
}
