import React, { useState } from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { LanguageProvider, useLanguage } from './context/LanguageContext';
import { FarmProvider } from './context/FarmContext';

// Layout
import Navbar from './components/layout/Navbar';
import Sidebar from './components/layout/Sidebar';
import MobileNav from './components/layout/MobileNav';

// Floating control icons
import { PanelLeftOpen, Eye, Layout } from 'lucide-react';

// Pages
import Dashboard from './pages/Dashboard';
import FarmMapPage from './pages/FarmMapPage';
import MonitoringPage from './pages/MonitoringPage';
import RiskDetectionPage from './pages/RiskDetectionPage';
import AIAdvisoryPage from './pages/AIAdvisoryPage';
import ActionPlansPage from './pages/ActionPlansPage';
import TaskExecutionPage from './pages/TaskExecutionPage';
import AgentCenterPage from './pages/AgentCenterPage';
import DiseaseDetectorPage from './pages/DiseaseDetectorPage';
import WeatherPage from './pages/WeatherPage';
import MarketPage from './pages/MarketPage';
import VoiceAssistantPage from './pages/VoiceAssistantPage';
import EscalationPage from './pages/EscalationPage';
import ReportsPage from './pages/ReportsPage';
import FarmSetupPage from './pages/FarmSetupPage';

function AppLayout({ children }) {
  const { t } = useLanguage();
  const [isSidebarVisible, setIsSidebarVisible] = useState(() => {
    const saved = localStorage.getItem('krishi_sidebar');
    return saved !== null ? JSON.parse(saved) : true;
  });

  const [isNavbarVisible, setIsNavbarVisible] = useState(() => {
    const saved = localStorage.getItem('krishi_navbar');
    return saved !== null ? JSON.parse(saved) : true;
  });

  const handleToggleSidebar = () => {
    setIsSidebarVisible(prev => {
      const next = !prev;
      localStorage.setItem('krishi_sidebar', JSON.stringify(next));
      return next;
    });
  };

  const handleToggleNavbar = (visible) => {
    setIsNavbarVisible(visible);
    localStorage.setItem('krishi_navbar', JSON.stringify(visible));
  };

  return (
    <div className="min-h-screen bg-slate-50 flex flex-col font-sans text-slate-800 antialiased selection:bg-emerald-500 selection:text-white">
      
      {/* Top Navbar with User Hide/Show Control */}
      {isNavbarVisible ? (
        <Navbar
          isSidebarVisible={isSidebarVisible}
          onToggleSidebar={handleToggleSidebar}
          onHideNavbar={() => handleToggleNavbar(false)}
        />
      ) : (
        /* Floating Restore Top Bar Button when hidden */
        <div className="fixed top-3 right-4 z-50 animate-in fade-in slide-in-from-top-2">
          <button
            onClick={() => handleToggleNavbar(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-slate-900/90 hover:bg-slate-900 text-white text-xs font-bold shadow-xl border border-slate-700 backdrop-blur-md transition-all hover:scale-105"
            title={t("navToggle.showNavbar", "Show Top Bar")}
          >
            <Eye className="w-3.5 h-3.5 text-emerald-400" />
            <span>{t("navToggle.showNavbar", "Show Top Bar")}</span>
          </button>
        </div>
      )}

      {/* Floating Restore Sidebar Button when hidden */}
      {!isSidebarVisible && (
        <div className="fixed top-16 left-3 z-40 animate-in fade-in slide-in-from-left-2">
          <button
            onClick={handleToggleSidebar}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-emerald-700 hover:bg-emerald-800 text-white text-xs font-bold shadow-xl border border-emerald-500/40 backdrop-blur-md transition-all hover:scale-105"
            title={t("navToggle.showSidebar", "Show Sidebar Menu")}
          >
            <PanelLeftOpen className="w-4 h-4" />
            <span>{t("navToggle.showSidebar", "Menu")}</span>
          </button>
        </div>
      )}

      {/* Main Content Layout with Sidebar side-by-side */}
      <div className="flex-1 flex w-full max-w-7xl mx-auto min-h-0">
        
        {/* Sidebar Component */}
        <Sidebar
          isVisible={isSidebarVisible}
          onClose={() => handleToggleSidebar()}
        />

        {/* Page Content Container: Never overlaps or gets hidden */}
        <main className="flex-1 p-4 sm:p-6 pb-28 lg:pb-12 min-w-0 transition-all">
          {children}
        </main>

      </div>

      {/* Mobile Bottom Navigation */}
      <MobileNav />

    </div>
  );
}

export default function App() {
  return (
    <LanguageProvider>
      <FarmProvider>
        <BrowserRouter>
          <AppLayout>
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/map" element={<FarmMapPage />} />
              <Route path="/monitoring" element={<MonitoringPage />} />
              <Route path="/risks" element={<RiskDetectionPage />} />
              <Route path="/advisory" element={<AIAdvisoryPage />} />
              <Route path="/action-plans" element={<ActionPlansPage />} />
              <Route path="/tasks" element={<TaskExecutionPage />} />
              <Route path="/agents" element={<AgentCenterPage />} />
              <Route path="/disease-detector" element={<DiseaseDetectorPage />} />
              <Route path="/weather" element={<WeatherPage />} />
              <Route path="/market" element={<MarketPage />} />
              <Route path="/assistant" element={<VoiceAssistantPage />} />
              <Route path="/escalation" element={<EscalationPage />} />
              <Route path="/reports" element={<ReportsPage />} />
              <Route path="/setup" element={<FarmSetupPage />} />
              <Route path="*" element={<Navigate to="/" replace />} />
            </Routes>
          </AppLayout>
        </BrowserRouter>
      </FarmProvider>
    </LanguageProvider>
  );
}
