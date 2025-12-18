import { useLocation,BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '../Home/home';
import Profile from '../Profile/profile';
import SignIn from '../SignIn/signin';
import SignUp from '../SignUp/signup';
import ResetPassword from '../ResetPassword/ResetPassword'
import Sidebar from '../../components/Sidebar/sidebar';
import ChatPage from '../ChatPage/chatpage';

const Layout = () => {
  const location = useLocation();
  const excludedPaths = ['/signin', '/signup', '/resetpassword'];
  const shouldShowSidebar = !excludedPaths.includes(location.pathname);

  return (
    <div style={{ display: 'flex' }}>
      {shouldShowSidebar && <Sidebar />}
      <main style={{ flex: 1 }}>
        <Routes>
          <Route path="/signin" element={<SignIn />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/resetpassword" element={<ResetPassword />} />
          <Route path="/" element={<Home />} />
          <Route path="/profile" element={<Profile />} />
          <Route path="/chat/:chatId" element={<ChatPage />} />
        </Routes>
      </main>
    </div>
  );
};

export default function Path() {
  return (
    <BrowserRouter>
      <Layout />
    </BrowserRouter>
  );
}
