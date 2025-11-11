import { Routes, Route } from "react-router-dom";
import Header from './components/Header'
import './style/App.css'

import Home from "./pages/Home.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import FeelbackForm from "./pages/FeelbackForm.jsx";
import Footer from "./components/Footer.jsx";

function App() {

  return (
    <>
      <Header />
      <>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/feelback-form" element={<FeelbackForm />} />
        </Routes>
      </>
      <Footer />
    </>
  )
}

export default App
