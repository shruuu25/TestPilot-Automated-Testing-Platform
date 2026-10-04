import React from 'react';
import { Play, Activity, Plus, BarChart3, Terminal, CheckCircle2, AlertCircle } from 'lucide-react';

export default function Navbar({ activeTab, setActiveTab, onOpenNewTestModal, healthStatus }) {
  const isHealthy = healthStatus?.status === 'healthy';

  return (
    <header className="border-b border-slate-800 bg-slate-900/90 sticky top-0 z-40 backdrop-blur">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Platform Name */}
          <div className="flex items-center space-x-3">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-600 to-indigo-400 flex items-center justify-center shadow-lg shadow-indigo-500/25">
              <Activity className="w-5 h-5 text-white" />
            </div>
            <div>
              <span data-testid="app-title" className="text-xl font-bold tracking-tight text-white flex items-center gap-2">
                TESTPILOT
                <span className="text-xs font-semibold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
                  v1.0
                </span>
              </span>
              <p className="text-xs text-slate-400">Automated Web & API Testing Platform</p>
            </div>
          </div>

          {/* Navigation Tabs */}
          <nav className="hidden md:flex space-x-1 bg-slate-800/60 p-1 rounded-lg border border-slate-700/50">
            <button
              onClick={() => setActiveTab('dashboard')}
              data-testid="nav-dashboard"
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'dashboard'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <BarChart3 className="w-4 h-4" />
              <span>Dashboard</span>
            </button>

            <button
              onClick={() => setActiveTab('execution')}
              data-testid="nav-execution"
              className={`flex items-center space-x-2 px-3 py-1.5 rounded-md text-sm font-medium transition-colors ${
                activeTab === 'execution'
                  ? 'bg-indigo-600 text-white shadow'
                  : 'text-slate-300 hover:text-white hover:bg-slate-700/50'
              }`}
            >
              <Terminal className="w-4 h-4" />
              <span>Execution Console</span>
            </button>
          </nav>

          {/* Right Controls: Health & New Test */}
          <div className="flex items-center space-x-3">
            <div className="flex items-center space-x-1.5 px-2.5 py-1 rounded-full text-xs font-medium bg-slate-800 border border-slate-700">
              {isHealthy ? (
                <>
                  <span className="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span>
                  <span className="text-emerald-400">System Healthy</span>
                </>
              ) : (
                <>
                  <span className="w-2 h-2 rounded-full bg-amber-400"></span>
                  <span className="text-amber-400">Connecting...</span>
                </>
              )}
            </div>

            <button
              onClick={onOpenNewTestModal}
              data-testid="btn-new-test"
              className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
            >
              <Plus className="w-4 h-4 text-indigo-400" />
              <span>New Test</span>
            </button>
          </div>
        </div>
      </div>
    </header>
  );
}
