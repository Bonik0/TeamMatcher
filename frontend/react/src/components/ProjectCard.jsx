import React from "react";
import { useNavigate } from "react-router-dom";
import { searchStyles } from "../styles/search";
import { projectCardStyles } from "../styles/projectCard";

export default function ProjectCard(
	{ project, highlightRoleIds = [], highlightCompetenceIds = [] },
) {
	const navigate = useNavigate();
	const onClick = () => {
		if (project && project.id) {
			navigate(`/project/${project.id}`);
		}
	};

	return (
		<div
			onClick={onClick}
			style={projectCardStyles.container}
			onMouseEnter={(e) => {
				e.currentTarget.style.boxShadow = "0 4px 12px rgba(0,0,0,0.08)";
			}}
			onMouseLeave={(e) => {
				e.currentTarget.style.boxShadow = "none";
			}}
		>
			<div style={projectCardStyles.titleRow}>
				<h2 style={projectCardStyles.title}>{project.name}</h2>
				<h2 style={projectCardStyles.countTitle}>
					{project.user_forms_count} участников
				</h2>
			</div>

			<p style={projectCardStyles.description}>{project.description}</p>

			<div style={projectCardStyles.rolesContainer}>
				{(project.roles || []).map((projectRole, i) => {
					const byRole = highlightRoleIds.includes(projectRole.role.id);
					const byComp = projectRole.competences.some(
						(projectRoleComp) =>
							highlightCompetenceIds.includes(projectRoleComp.competence.id),
					);

					const highlight = byRole || byComp;

					return (
						<div
							key={i}
							style={{
								background: highlight
									? searchStyles.highlightRoleBg
									: projectCardStyles.roleChip.background,
								border: highlight
									? `1px solid ${searchStyles.highlightRoleBorder}`
									: projectCardStyles.roleChip.border,
								color: projectCardStyles.roleChip.color,
								padding: projectCardStyles.roleChip.padding,
								borderRadius: projectCardStyles.roleChip.borderRadius,
								fontSize: "1.2rem",
								display: "flex",
								alignItems: "center",
								marginRight: "0.4rem",
							}}
						>
							{projectRole.role.name}
						</div>
					);
				})}
			</div>
		</div>
	);
}
