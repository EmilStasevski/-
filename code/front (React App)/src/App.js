import "./styles.css";
import Navbar from "./Navbar";
import Home from "./pages/Home";
import President from "./pages/President";
import Region from "./pages/Region";
import Parliament from "./pages/Parliament";
import ConstRF from "./pages/ConstRF";

import { Route, Routes } from "react-router-dom";

function App() {
  return (
    <>
      <Navbar />
      <div className="container">
        <Routes>
          <Route path="/" element={<Home />} />

          <Route path="/President" element={<President />} />
          <Route path="/Parliament" element={<Parliament />} />
          <Route path="/Region" element={<Region />} />
          <Route path="/ConstRF" element={<ConstRF />} />
        </Routes>
      </div>
    </>
  );
}

export default App;
