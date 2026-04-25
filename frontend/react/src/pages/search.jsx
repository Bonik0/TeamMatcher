import React, { useEffect, useState } from "react";
import SearchSelect from "../components/SearchSelect";
import ProjectCard from "../components/ProjectCard";
import { defaultStyles } from "../styles/default";
import { searchStyles } from "../styles/search";

export default function SearchPage() {
	const PAGE_SIZE = 10;

	const [name, setName] = useState("");
	const [roles, setRoles] = useState([]);
	const [comps, setComps] = useState([]);
	const [projects, setProjects] = useState([]);
	const [page, setPage] = useState(1);
	const [loading, setLoading] = useState(false);
	const [error, setError] = useState("");

	useEffect(() => {
		const fetchProjects = async () => {
			setLoading(true);
			setError("");
			try {
				const params = new URLSearchParams();
				if (name) {
					params.append("q", name);
				}
				roles.forEach((role) => {
					params.append("role_ids", String(role.id));
				});

				comps.forEach((comp) => {
					params.append("competence_ids", String(comp.id));
				});

				params.append("limit", PAGE_SIZE);
				params.append("offset", PAGE_SIZE * (page - 1));

				const response = await fetch(
					`http://localhost:8000/api/search/project?${params.toString()}`,
				);
				if (!response.ok) {
					setError("Ошибка поиска");
					setProjects([]);
					return;
				}
				const response_dict = await response.json();
				setProjects(response_dict["projects"]);
			} catch (error) {
				setError("Ошибка сети");
			} finally {
				setLoading(false);
			}
		};
		fetchProjects();
	}, [name, roles, comps, page]);

	const setNameHandle = (value) => {
		setName(value);
		setPage(1);
	};

	const onSelectRole = (roleObj) => {
		if (!roles.some((role) => String(role.id) === String(roleObj.id))) {
			setRoles((prev) => [...prev, roleObj]);
			setPage(1);
		}
	};
	const onSelectComp = (compObj) => {
		if (!comps.some((comp) => String(comp.id) === String(compObj.id))) {
			setComps((prev) => [...prev, compObj]);
			setPage(1);
		}
	};

	const removeRole = (id) => {
		setRoles((prev) => prev.filter((role) => String(role.id) !== String(id)));
		setPage(1);
	};
	const removeComp = (id) => {
		setComps((prev) => prev.filter((comp) => String(comp.id) !== String(id)));
		setPage(1);
	};

	const goNext = () => {
		if (projects.length === 0) {
			return;
		}
		setPage((page) => page + 1);
	};
	const goPrev = () => {
		setPage((page) => Math.max(1, page - 1));
	};

	return (
		<div style={defaultStyles.container}>
			<div style={defaultStyles.itemsContainer}>
				<div style={defaultStyles.itemsSection}>
					<h2 style={defaultStyles.title}>Поиск проектов</h2>

					<div style={{ marginBottom: "1rem", marginTop: "1rem" }}>
						<input
							type="text"
							placeholder="Поиск по названию проекта"
							value={name}
							onChange={(e) => setNameHandle(e.target.value)}
							style={{ ...defaultStyles.input, ...searchStyles.nameInput }}
						/>
					</div>

					<div style={searchStyles.filtersRow}>
						<div style={{ flex: 1 }}>
							<SearchSelect
								placeholder="Поиск по ролям"
								fetchUrl="/api/search/role"
								onSelect={onSelectRole}
								selectedItems={roles}
								executedName="roles"
							/>
							{roles && roles.length > 0 && (
								<div style={searchStyles.chipContainer}>
									{roles.map((role) => (
										<div
											key={String(role.id) + role.name}
											style={searchStyles.chip}
										>
											<span>{role.name}</span>
											<button
												type="button"
												aria-label="remove-role"
												onClick={() => removeRole(role.id)}
												style={searchStyles.chipRemoveButton}
											>
												×
											</button>
										</div>
									))}
								</div>
							)}
						</div>
						<div style={{ flex: 1 }}>
							<SearchSelect
								placeholder="Поиск по компетенциям"
								fetchUrl="/api/search/competence"
								onSelect={onSelectComp}
								selectedItems={comps}
								executedName="competencies"
							/>
							{comps && comps.length > 0 && (
								<div style={searchStyles.chipContainer}>
									{comps.map((comp) => (
										<div
											key={String(comp.id) + comp.name}
											style={searchStyles.chip}
										>
											<span>{comp.name}</span>
											<button
												type="button"
												aria-label="remove-comp"
												onClick={() => removeComp(comp.id)}
												style={searchStyles.chipRemoveButton}
											>
												×
											</button>
										</div>
									))}
								</div>
							)}
						</div>
					</div>

					{!loading && projects.length === 0 && (
						<div style={defaultStyles.noText}>Ничего не найдено</div>
					)}
				</div>

				<div style={searchStyles.results}>
					{loading && <div style={defaultStyles.loading}>Загрузка...</div>}
					{error && (
						<div style={{ ...defaultStyles.noText, color: "red" }}>{error}</div>
					)}

					{projects.map((project) => (
						<ProjectCard
							key={project.id}
							project={project}
							highlightRoleIds={roles.map((role) => role.id)}
							highlightCompetenceIds={comps.map((comp) => comp.id)}
						/>
					))}

					{
						<div style={searchStyles.paginationContainer}>
							<div style={searchStyles.paginationInner}>
								<button
									type="button"
									onClick={goPrev}
									style={page === 1
										? searchStyles.paginationButtonDisabled
										: searchStyles.paginationButton}
									disabled={page === 1}
								>
									Назад
								</button>
								<div style={searchStyles.pageTitle}>Страница {page}</div>
								<button
									type="button"
									onClick={goNext}
									style={searchStyles.paginationButton}
								>
									Вперед
								</button>
							</div>
						</div>
					}
				</div>
			</div>
		</div>
	);
}
