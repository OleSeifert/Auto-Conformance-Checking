/*
This is the main entry point for the React application.
*/

import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import CelonisCredentials from './CelonisCredentials';
import UploadPage from './UploadPage';
import MappingPage from './MappingPage';
import ResultsPage from './ResultsPage';
import SidebarLayout from './SidebarLayout';

function App() {
  return (
    <Router>
      <SidebarLayout>
        <Routes>
          <Route path="/" element={<CelonisCredentials />} />
          <Route path="/upload" element={<UploadPage />} />
          <Route path="/mapping" element={<MappingPage />} />
          <Route path="/results" element={<ResultsPage />} />
        </Routes>
      </SidebarLayout>
    </Router>
  );
}

export default App;