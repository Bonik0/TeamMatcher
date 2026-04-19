import React from 'react';
import { BrowserRouter as Router, Routes, Route, Outlet } from 'react-router-dom';
import EmailVerificationPage from './pages/emailVerification'
import LoginPage from './pages/login';
import RegisterPage from './pages/registrate';
import ChangePasswordPage from './pages/changePassword';
import TagsPage from './pages/tags';
import BannedUsersPage from './pages/ban';
import MeetingsPage from './pages/meetings';
import UserSearchPage from './pages/search';
import SearchProfilePage from './pages/searchProfile';
import SideMenu from './components/menu';


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
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/forgot-password" element={<ChangePasswordPage />} />
      <Route path="/email-verify" element={<EmailVerificationPage />} />

      <Route element={<LayoutWithMenu />}>
          <Route path="/meetings" element={<MeetingsPage />} />
          <Route path='/profile' element={<SearchProfilePage/>}/>
          <Route path="/tags" element={<TagsPage />} />
          <Route path="/banned-users" element={<BannedUsersPage />} />
          <Route path="/" element={<UserSearchPage />} />
      </Route>
      </Routes>
    </Router>
  );
}
export default App;
