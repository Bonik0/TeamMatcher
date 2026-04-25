import React, { useEffect, useState } from "react";
import SearchSelect from "../components/SearchSelect";
import { defaultStyles } from "../styles/default";
import { userCompetenceStyles } from "../styles/userCompetences";
import { fetchWithTokens } from "../utils/auth";

export default function UserCompetencesPage() {
	const [competences, setCompetences] = useState([]);
	const [pending, setPending] = useState(null);
	const [pendingLevel, setPendingLevel] = useState(1);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	useEffect(() => {
		const load = async () => {
			setLoading(true);
			setError("");
			try {
				const response = await fetchWithTokens(
					"GET",
					"http://localhost:8000/api/user/competence",
				);
				if (!response.ok) {
					setError("Не удалось загрузить компетенции");
					setCompetences([]);
					setLoading(false);
					return;
				}
				const response_dict = await response.json();
				const list = (response_dict.competences || []).map(
					(it) => (
						{
							id: it.competence.id,
							name: it.competence.name,
							level: it.level,
						}
					),
				);
				setCompetences(list);
			} catch (e) {
				setError("Ошибка сети");
			} finally {
				setLoading(false);
			}
		};
		load();
	}, []);

	const cancelButtonHandler = () => {
		setPending(null);
		setPendingLevel(1);
	};

	const addCompetence = async (item, level) => {
		try {
			const response = await fetchWithTokens(
				"POST",
				"http://localhost:8000/api/user/competence",
				JSON.stringify(
					{
						competences: [{
							competence_id: Number(item.id),
							level: Number(level),
						}],
					},
				),
			);
			if (!response.ok) {
				setError("Не удалось добавить компетенцию");
				return false;
			}
			setCompetences((
				prev,
			) => [...prev, { id: item.id, name: item.name, level: Number(level) }]);
			return true;
		} catch (e) {
			setError("Ошибка сети");
			return false;
		} finally {
			cancelButtonHandler();
		}
	};

	const removeCompetence = async (id) => {
		try {
			const response = await fetchWithTokens(
				"DELETE",
				"http://localhost:8000/api/user/competence",
				JSON.stringify({ competence_ids: [Number(id)] }),
			);
			if (!response.ok) {
				setError("Не удалось удалить компетенцию");
				return;
			}
			setCompetences((prev) =>
				prev.filter((comp) => String(comp.id) !== String(id))
			);
		} catch (e) {
			setError("Ошибка сети");
		}
	};

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					<h2 style={defaultStyles.title}>Мои компетенции</h2>

					{loading && <div style={defaultStyles.loading}>Загрузка...</div>}
					{error && (
						<div style={{ ...defaultStyles.noText, color: "red" }}>{error}</div>
					)}

					{!error && !loading && (
						<div>
							<div style={userCompetenceStyles.searchRow}>
								<SearchSelect
									placeholder="Добавить компетенцию"
									fetchUrl="/api/search/competence"
									onSelect={(item) => setPending(item)}
									executedName="competencies"
									selectedItems={competences.map((comp) => ({
										id: comp.id,
										name: comp.name,
									}))}
								/>

								{pending && (
									<div style={userCompetenceStyles.levelSelector}>
										<div>
											Вы выбрали:{" "}
											<strong style={{ marginLeft: 6 }}>{pending.name}</strong>
										</div>
										<div
											style={{
												display: "flex",
												alignItems: "center",
												gap: "0.5rem",
												marginLeft: 12,
											}}
										>
											<button
												type="button"
												onClick={() => setPendingLevel(1)}
												style={{
													...userCompetenceStyles.levelButton,
													...(pendingLevel === 1
														? userCompetenceStyles.levelButtonActive
														: {}),
												}}
											>
												начальный
											</button>
											<button
												type="button"
												onClick={() => setPendingLevel(2)}
												style={{
													...userCompetenceStyles.levelButton,
													...(pendingLevel === 2
														? userCompetenceStyles.levelButtonActive
														: {}),
												}}
											>
												продвинутый
											</button>
											<button
												type="button"
												onClick={() => setPendingLevel(3)}
												style={{
													...userCompetenceStyles.levelButton,
													...(pendingLevel === 3
														? userCompetenceStyles.levelButtonActive
														: {}),
												}}
											>
												профессиональный
											</button>
											<button
												type="button"
												style={userCompetenceStyles.addConfirmButton}
												onClick={async () => {
													await addCompetence(pending, pendingLevel);
												}}
											>
												Добавить
											</button>
											<button
												type="button"
												onClick={cancelButtonHandler}
												style={userCompetenceStyles.addCancelButton}
											>
												Отмена
											</button>
										</div>
									</div>
								)}
							</div>

							{competences.length === 0 && !loading && !error && (
								<div style={defaultStyles.noText}>
									У вас пока нет компетенций
								</div>
							)}

							<div style={userCompetenceStyles.competenceList}>
								{competences.map((comp) => {
									const level = comp.level ?? 1;
									const levelStyle = userCompetenceStyles.levels[level];
									return (
										<div
											key={comp.id}
											style={{
												...userCompetenceStyles.competenceChip,
												background: levelStyle.bg,
												border: `1px solid ${levelStyle.border}`,
												color: levelStyle.text,
											}}
										>
											<span style={{ fontWeight: 600 }}>{comp.name}</span>
											<span
												style={{
													marginLeft: 8,
													fontSize: "0.95rem",
													color: "#666",
												}}
											>
												({level === 1
													? "начальный"
													: level === 2
													? "продвинутый"
													: "профессиональный"})
											</span>
											<button
												type="button"
												style={userCompetenceStyles.removeButton}
												onClick={() => removeCompetence(comp.id)}
												aria-label="remove-competence"
											>
												×
											</button>
										</div>
									);
								})}
							</div>
						</div>
					)}
				</div>
			</div>
		</div>
	);
}
