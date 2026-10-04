import React, { useState, useEffect } from 'react';
import { Play, RefreshCw, CheckCircle, XCircle, Layers, Activity, Percent } from 'lucide-react';
import KPICard from '../components/KPICard';
import TestResultsTable from '../components/TestResultsTable';
import RecentRunsTable from '../components/RecentRunsTable';
import { api } from '../services/api';

export default function DashboardPage() {
  const [stats, setStats] = useState({
    total_test_cases: 0,
    total_test_runs: 0,
    total_passed_tests: 0,
    total_failed_tests: 0,
    pass_percentage: 0.0,
  });
  const [results, setResults] = useState([]);
  const [runs, setRuns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [executing, setExecuting] = useState(false);
  const [runBanner, setRunBanner] = useState(null);

  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [statusFilter, setStatusFilter] = useState('ALL');
  const [typeFilter, setTypeFilter] = useState('ALL');

  const loadDashboardData = async () => {
    try {
      setLoading(true);
      const [statsData, resultsData, runsData] = await Promise.all([
        api.getStats(),
        api.getResults({ limit: 100 }),
        api.getRuns(10),
      ]);
      setStats(statsData);
      setResults(resultsData);
      setRuns(runsData);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const handleRunTests = async () => {
    try {
      setExecuting(true);
      setRunBanner({
        type: 'running',
        message: 'Executing automated test suite... Running assertions and capturing telemetry.',
      });

      const newRun = await api.triggerTestRun('ALL');

      setRunBanner({
        type: 'success',
        message: `Test run #${newRun.id} completed: ${newRun.passed_tests}/${newRun.total_tests} passed in ${newRun.results?.length} tests.`,
      });

      // Refresh data
      await loadDashboardData();
    } catch (err) {
      setRunBanner({
        type: 'error',
        message: err.response?.data?.detail || 'Failed to execute test suite.',
      });
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-8">
      {/* Top Action Bar */}
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h1 className="text-2xl font-extrabold text-white tracking-tight">Testing Analytics Dashboard</h1>
          <p className="text-sm text-slate-400">
            Real-time execution telemetry across REST API and Selenium UI test suites
          </p>
        </div>

        <div className="flex items-center space-x-3">
          <button
            onClick={loadDashboardData}
            data-testid="btn-refresh"
            disabled={loading}
            className="flex items-center space-x-1.5 bg-slate-800 hover:bg-slate-700 text-slate-300 border border-slate-700 px-3.5 py-2 rounded-lg text-sm font-medium transition disabled:opacity-50"
          >
            <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
            <span>Refresh</span>
          </button>

          <button
            onClick={handleRunTests}
            data-testid="btn-run-tests"
            disabled={executing}
            className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white px-4 py-2 rounded-lg text-sm font-semibold shadow-lg shadow-indigo-500/25 transition disabled:opacity-50"
          >
            {executing ? (
              <>
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Executing Suite...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-white" />
                <span>Run Tests</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Execution Banner */}
      {runBanner && (
        <div
          data-testid="run-status-banner"
          className={`p-4 rounded-xl border text-sm flex items-center justify-between ${
            runBanner.type === 'running'
              ? 'bg-amber-500/10 border-amber-500/30 text-amber-300 animate-pulse'
              : runBanner.type === 'success'
              ? 'bg-emerald-500/10 border-emerald-500/30 text-emerald-300'
              : 'bg-rose-500/10 border-rose-500/30 text-rose-300'
          }`}
        >
          <div className="flex items-center gap-2">
            {runBanner.type === 'running' && (
              <span className="w-3 h-3 rounded-full bg-amber-400 animate-ping"></span>
            )}
            {runBanner.type === 'success' && <CheckCircle className="w-4 h-4 text-emerald-400" />}
            {runBanner.type === 'error' && <XCircle className="w-4 h-4 text-rose-400" />}
            <span>{runBanner.message}</span>
          </div>

          <button
            onClick={() => setRunBanner(null)}
            className="text-xs opacity-70 hover:opacity-100 uppercase font-semibold"
          >
            Dismiss
          </button>
        </div>
      )}

      {/* KPI Cards Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-4">
        <KPICard
          title="Total Test Cases"
          value={stats.total_test_cases}
          icon={Layers}
          color="indigo"
          testId="kpi-total-cases"
          subtitle="Registered test definitions"
        />
        <KPICard
          title="Total Test Runs"
          value={stats.total_test_runs}
          icon={Activity}
          color="blue"
          testId="kpi-total-runs"
          subtitle="Execution sessions"
        />
        <KPICard
          title="Passed Tests"
          value={stats.total_passed_tests}
          icon={CheckCircle}
          color="emerald"
          testId="kpi-passed-tests"
          subtitle="Successful assertions"
        />
        <KPICard
          title="Failed Tests"
          value={stats.total_failed_tests}
          icon={XCircle}
          color="rose"
          testId="kpi-failed-tests"
          subtitle="Assertion failures"
        />
        <KPICard
          title="Pass Percentage"
          value={`${stats.pass_percentage}%`}
          icon={Percent}
          color="emerald"
          testId="kpi-pass-rate"
          subtitle="Overall suite health"
        />
      </div>

      {/* Dual Table Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 space-y-4">
          <div className="flex justify-between items-center">
            <h2 className="text-lg font-bold text-white tracking-tight">Granular Test Results</h2>
            <span className="text-xs text-slate-400 font-mono">
              Showing {results.length} total outcomes
            </span>
          </div>
          <TestResultsTable
            results={results}
            loading={loading}
            searchTerm={searchTerm}
            setSearchTerm={setSearchTerm}
            statusFilter={statusFilter}
            setStatusFilter={setStatusFilter}
            typeFilter={typeFilter}
            setTypeFilter={setTypeFilter}
          />
        </div>

        <div className="space-y-4">
          <h2 className="text-lg font-bold text-white tracking-tight">Execution History</h2>
          <RecentRunsTable runs={runs} loading={loading} />
        </div>
      </div>
    </div>
  );
}
