import React from "react";
import {
	BrowserRouter as Router,
	Outlet,
	Route,
	Routes,
} from "react-router-dom";
import EmailVerificationPage from "./pages/emailVerification";
import LoginPage from "./pages/login";
import RegisterPage from "./pages/registrate";
import ChangePasswordPage from "./pages/changePassword";
import SideMenu from "./components/menu";
import SearchPage from "./pages/search";
import UserCompetencesPage from "./pages/userCompetences";
import TeamsPage from "./pages/teams";
import ProjectPage from "./pages/project";
import AppliedProjectsPage from "./pages/appliedProjects";
import OrganizerProjectsPage from "./pages/organizerProjects";
import ProjectCreatePage from "./pages/project_create";

const LayoutWithMenu = () => {
	return (
		<>
			<SideMenu />
			<Outlet />
		</>
	);
};

function App() {
	return (
		<Router>
			<Routes>
				<Route element={<LayoutWithMenu />}>
					<Route path="/" element={<SearchPage />} />
					<Route path="/project/:id" element={<ProjectPage />} />
					<Route path="/teams" element={<TeamsPage />} />
					<Route path="/user/competences" element={<UserCompetencesPage />} />
					<Route path="/user/roles" element={<AppliedProjectsPage />} />
					<Route
						path="/organizer/projects"
						element={<OrganizerProjectsPage />}
					/>
					<Route path="/project/create" element={<ProjectCreatePage />} />
				</Route>
				<Route path="/login" element={<LoginPage />} />
				<Route path="/register" element={<RegisterPage />} />
				<Route path="/forgot-password" element={<ChangePasswordPage />} />
				<Route path="/email-verify" element={<EmailVerificationPage />} />
			</Routes>
		</Router>
	);
}
export default App;
