import React, { useState, useEffect } from 'react';
import Navbar from './components/Navbar';
import DashboardPage from './pages/DashboardPage';
import TestExecutionPage from './pages/TestExecutionPage';
import NewTestCaseModal from './components/NewTestCaseModal';
import { api } from './services/api';

export default function App() {
  const [activeTab, setActiveTab] = useState('dashboard');
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [health, setHealth] = useState({ status: 'connecting', database: 'connecting' });

  const checkHealth = async () => {
    try {
      const data = await api.getHealth();
      setHealth(data);
    } catch {
      setHealth({ status: 'degraded', database: 'unavailable' });
    }
  };

  useEffect(() => {
    checkHealth();
    const interval = setInterval(checkHealth, 30000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="min-h-screen bg-slate-900 text-slate-100 flex flex-col font-sans selection:bg-indigo-500 selection:text-white">
      {/* Navbar */}
      <Navbar
        activeTab={activeTab}
        setActiveTab={setActiveTab}
        onOpenNewTestModal={() => setIsModalOpen(true)}
        healthStatus={health}
      />

      {/* Main View Area */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {activeTab === 'dashboard' ? <DashboardPage /> : <TestExecutionPage />}
      </main>

      {/* New Test Case Modal */}
      <NewTestCaseModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
        onCreated={() => {
          // Trigger a lightweight recheck or tab focus
          if (activeTab === 'dashboard') {
            window.location.reload();
          }
        }}
      />

      {/* Footer */}
      <footer className="border-t border-slate-800 bg-slate-900/60 py-6 text-center text-xs text-slate-400">
        <div className="max-w-7xl mx-auto px-4 flex flex-col sm:flex-row items-center justify-between gap-2">
          <p>© 2026 TestPilot Platform. Built for SDET automation engineering and CI validation.</p>
          <div className="flex items-center space-x-4">
            <span>FastAPI Backend</span>
            <span>•</span>
            <span>Pytest + Selenium</span>
            <span>•</span>
            <span>React + Vite</span>
            <span>•</span>
            <span>MySQL</span>
          </div>
        </div>
      </footer>
    </div>
  );
}
