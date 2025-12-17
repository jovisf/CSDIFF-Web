import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from '../Home/home';
import Profile from '../Profile/profile';
import SignIn from '../SignIn/signin';
import SignUp from '../SignUp/signup';
import ResetPassword from '../ResetPassword/ResetPassword'

export default function Path() {
  return (
    <BrowserRouter>
        <Routes>
            <Route path='/signin' element={<SignIn/>}/>
            <Route path='/signup' element={<SignUp/>}/>
            <Route path='/resetpassword' element={<ResetPassword/>}/>
            <Route path='/' element={<Home/>}/>
            <Route path='/profile' element={<Profile/>}/>    
        </Routes>
    </BrowserRouter>
  )
}
