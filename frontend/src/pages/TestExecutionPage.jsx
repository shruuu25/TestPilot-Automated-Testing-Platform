import React, { useState } from 'react';
import { Terminal, Play, CheckCircle2, XCircle, Clock, ShieldCheck, Cpu } from 'lucide-react';
import { api } from '../services/api';

export default function TestExecutionPage() {
  const [suiteType, setSuiteType] = useState('ALL');
  const [executing, setExecuting] = useState(false);
  const [statusText, setStatusText] = useState('IDLE');
  const [lastRun, setLastRun] = useState(null);
  const [logs, setLogs] = useState([
    'TestPilot Engine v1.0.0 initialized.',
    'System ready for test execution trigger.',
    'Click "Run Selected Suite" to begin test execution.',
  ]);

  const addLog = (msg) => {
    const time = new Date().toLocaleTimeString();
    setLogs((prev) => [...prev, `[${time}] ${msg}`]);
  };

  const handleRunSuite = async () => {
    try {
      setExecuting(true);
      setStatusText('RUNNING');
      setLogs([]);
      addLog(`Initiating test execution suite for type: [${suiteType}]`);
      addLog('Resolving registered test case definitions from database...');
      addLog('Setting up execution worker and assertion listeners...');

      const result = await api.triggerTestRun(suiteType);

      addLog(`Suite execution completed with status: ${result.status}`);
      addLog(`Total Tests Executed: ${result.total_tests}`);
      addLog(`Passed Assertions: ${result.passed_tests}`);
      addLog(`Failed Assertions: ${result.failed_tests}`);

      if (result.results && result.results.length > 0) {
        result.results.forEach((r) => {
          const outcome = r.status === 'PASSED' ? '✓ PASS' : '✗ FAIL';
          addLog(`${outcome} | [${r.test_type}] ${r.test_case_name} (${r.duration}s)`);
          if (r.error_message) {
            addLog(`     Error: ${r.error_message}`);
          }
        });
      }

      addLog('All test results and telemetry committed to database.');
      setStatusText(result.status);
      setLastRun(result);
    } catch (err) {
      addLog(`Execution error: ${err.message}`);
      setStatusText('FAILED');
    } finally {
      setExecuting(false);
    }
  };

  return (
    <div className="space-y-6">
      {/* Header */}
      <div>
        <h1 className="text-2xl font-extrabold text-white tracking-tight">Test Execution Console</h1>
        <p className="text-sm text-slate-400">
          Targeted suite execution with real-time assertion logging and database sync
        </p>
      </div>

      {/* Control Panel */}
      <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-6 shadow-lg space-y-6">
        <div>
          <label className="block text-xs font-semibold text-slate-400 uppercase tracking-wider mb-3">
            Select Test Suite Scope:
          </label>
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
            <button
              type="button"
              data-testid="select-suite-all"
              onClick={() => setSuiteType('ALL')}
              className={`p-3.5 rounded-lg border text-left transition flex items-center justify-between ${
                suiteType === 'ALL'
                  ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg'
                  : 'bg-slate-900/60 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-200'
              }`}
            >
              <div>
                <p className="text-sm font-semibold">Complete Suite (ALL)</p>
                <p className="text-xs text-slate-400">Run all registered API & UI tests</p>
              </div>
              <ShieldCheck className="w-5 h-5 text-indigo-400" />
            </button>

            <button
              type="button"
              data-testid="select-suite-api"
              onClick={() => setSuiteType('API')}
              className={`p-3.5 rounded-lg border text-left transition flex items-center justify-between ${
                suiteType === 'API'
                  ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg'
                  : 'bg-slate-900/60 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-200'
              }`}
            >
              <div>
                <p className="text-sm font-semibold">REST API Suite</p>
                <p className="text-xs text-slate-400">HTTP endpoints, status codes, schemas</p>
              </div>
              <Cpu className="w-5 h-5 text-blue-400" />
            </button>

            <button
              type="button"
              data-testid="select-suite-ui"
              onClick={() => setSuiteType('UI')}
              className={`p-3.5 rounded-lg border text-left transition flex items-center justify-between ${
                suiteType === 'UI'
                  ? 'bg-indigo-600/20 border-indigo-500 text-white shadow-lg'
                  : 'bg-slate-900/60 border-slate-700 text-slate-400 hover:border-slate-600 hover:text-slate-200'
              }`}
            >
              <div>
                <p className="text-sm font-semibold">Selenium Web UI Suite</p>
                <p className="text-xs text-slate-400">Browser flows, DOM validation, POM</p>
              </div>
              <Terminal className="w-5 h-5 text-purple-400" />
            </button>
          </div>
        </div>

        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 pt-4 border-t border-slate-700/60">
          <div className="flex items-center space-x-3">
            <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">
              Status:
            </span>
            <span
              data-testid="execution-status-badge"
              className={`text-xs px-3 py-1 rounded-full font-bold uppercase tracking-wider ${
                statusText === 'COMPLETED'
                  ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/30'
                  : statusText === 'RUNNING'
                  ? 'bg-amber-500/10 text-amber-400 border border-amber-500/30 animate-pulse'
                  : statusText === 'FAILED'
                  ? 'bg-rose-500/10 text-rose-400 border border-rose-500/30'
                  : 'bg-slate-800 text-slate-400 border border-slate-700'
              }`}
            >
              {statusText}
            </span>
          </div>

          <button
            onClick={handleRunSuite}
            data-testid="btn-trigger-suite"
            disabled={executing}
            className="flex items-center space-x-2 bg-indigo-600 hover:bg-indigo-500 text-white px-5 py-2.5 rounded-lg text-sm font-semibold shadow-lg shadow-indigo-500/25 transition disabled:opacity-50"
          >
            {executing ? (
              <>
                <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
                <span>Executing {suiteType} Suite...</span>
              </>
            ) : (
              <>
                <Play className="w-4 h-4 fill-white" />
                <span>Run Selected Suite</span>
              </>
            )}
          </button>
        </div>
      </div>

      {/* Execution Summary If Available */}
      {lastRun && (
        <div
          data-testid="execution-summary"
          className="bg-slate-800/80 border border-slate-700/60 rounded-xl p-5 shadow-lg grid grid-cols-2 sm:grid-cols-4 gap-4 text-center"
        >
          <div>
            <p className="text-xs text-slate-400 uppercase">Run ID</p>
            <p className="text-xl font-bold font-mono text-white mt-1">#{lastRun.id}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase">Total Tests</p>
            <p className="text-xl font-bold text-white mt-1">{lastRun.total_tests}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase">Passed</p>
            <p className="text-xl font-bold text-emerald-400 mt-1">{lastRun.passed_tests}</p>
          </div>
          <div>
            <p className="text-xs text-slate-400 uppercase">Failed</p>
            <p className="text-xl font-bold text-rose-400 mt-1">{lastRun.failed_tests}</p>
          </div>
        </div>
      )}

      {/* Terminal Output Log Container */}
      <div className="bg-slate-950 border border-slate-800 rounded-xl overflow-hidden shadow-2xl">
        <div className="px-4 py-2.5 bg-slate-900 border-b border-slate-800 flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <span className="w-3 h-3 rounded-full bg-rose-500 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-amber-500 inline-block"></span>
            <span className="w-3 h-3 rounded-full bg-emerald-500 inline-block"></span>
            <span className="text-xs font-mono text-slate-400 ml-2">testpilot-runner-output</span>
          </div>
          <span className="text-xs text-slate-500 font-mono">ANSI Console</span>
        </div>

        <div
          data-testid="execution-terminal"
          className="p-4 font-mono text-xs text-emerald-400 space-y-1 max-h-96 overflow-y-auto"
        >
          {logs.map((line, idx) => (
            <div key={idx} className="leading-relaxed">
              {line}
            </div>
          ))}
        </div>
      </div>
    </div>
  );
}
