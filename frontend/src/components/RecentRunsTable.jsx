import React from 'react';
import { History, CheckCircle, XCircle, Clock } from 'lucide-react';

export default function RecentRunsTable({ runs = [], loading = false }) {
  return (
    <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl overflow-hidden shadow-lg">
      <div className="p-4 border-b border-slate-700/60 flex items-center justify-between">
        <div className="flex items-center space-x-2">
          <History className="w-4 h-4 text-indigo-400" />
          <h3 className="text-sm font-semibold text-white">Recent Test Runs</h3>
        </div>
        <span className="text-xs text-slate-400">Total Runs: {runs.length}</span>
      </div>

      <div className="overflow-x-auto">
        <table data-testid="runs-table" className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="bg-slate-900/50 text-slate-400 border-b border-slate-700/60 text-xs font-semibold uppercase tracking-wider">
              <th className="py-3 px-4">Run ID</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Passed / Total</th>
              <th className="py-3 px-4">Pass Rate</th>
              <th className="py-3 px-4">Started At</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {loading ? (
              <tr>
                <td colSpan="5" className="py-6 text-center text-slate-400 text-xs">
                  Loading test runs...
                </td>
              </tr>
            ) : runs.length === 0 ? (
              <tr>
                <td colSpan="5" className="py-6 text-center text-slate-400 text-xs">
                  No execution runs recorded yet.
                </td>
              </tr>
            ) : (
              runs.map((run) => {
                const passRate =
                  run.total_tests > 0
                    ? Math.round((run.passed_tests / run.total_tests) * 100)
                    : 0;

                return (
                  <tr
                    key={run.id}
                    data-testid="run-row"
                    className="hover:bg-slate-700/30 transition-colors"
                  >
                    <td className="py-3 px-4 font-mono text-white text-xs font-semibold">
                      #{run.id}
                    </td>

                    <td className="py-3 px-4">
                      <span
                        className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                          run.status === 'COMPLETED'
                            ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                            : run.status === 'RUNNING'
                            ? 'bg-amber-500/10 text-amber-400 border border-amber-500/20 animate-pulse'
                            : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                        }`}
                      >
                        {run.status}
                      </span>
                    </td>

                    <td className="py-3 px-4 text-xs text-slate-300">
                      <span className="text-emerald-400 font-semibold">{run.passed_tests}</span>
                      <span className="text-slate-500"> / </span>
                      <span>{run.total_tests}</span>
                    </td>

                    <td className="py-3 px-4">
                      <div className="flex items-center space-x-2">
                        <div className="w-16 bg-slate-700 rounded-full h-1.5 overflow-hidden">
                          <div
                            className={`h-1.5 rounded-full ${
                              passRate === 100
                                ? 'bg-emerald-400'
                                : passRate > 70
                                ? 'bg-indigo-400'
                                : 'bg-rose-400'
                            }`}
                            style={{ width: `${passRate}%` }}
                          ></div>
                        </div>
                        <span className="text-xs font-mono text-slate-300">{passRate}%</span>
                      </div>
                    </td>

                    <td className="py-3 px-4 text-slate-400 text-xs">
                      {run.started_at ? new Date(run.started_at).toLocaleTimeString() : 'N/A'}
                    </td>
                  </tr>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
