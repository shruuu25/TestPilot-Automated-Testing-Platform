import React, { useState } from 'react';
import { Search, Filter, CheckCircle2, XCircle, Clock, ChevronDown, ChevronUp, AlertTriangle } from 'lucide-react';

export default function TestResultsTable({
  results = [],
  loading = false,
  searchTerm,
  setSearchTerm,
  statusFilter,
  setStatusFilter,
  typeFilter,
  setTypeFilter,
}) {
  const [expandedRow, setExpandedRow] = useState(null);

  const toggleRow = (id) => {
    setExpandedRow(expandedRow === id ? null : id);
  };

  const filteredResults = results.filter((r) => {
    const matchesSearch =
      r.test_case_name?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.status?.toLowerCase().includes(searchTerm.toLowerCase()) ||
      r.error_message?.toLowerCase().includes(searchTerm.toLowerCase());

    const matchesStatus =
      statusFilter === 'ALL' || r.status?.toUpperCase() === statusFilter.toUpperCase();

    const matchesType =
      typeFilter === 'ALL' || r.test_type?.toUpperCase() === typeFilter.toUpperCase();

    return matchesSearch && matchesStatus && matchesType;
  });

  return (
    <div className="bg-slate-800/80 border border-slate-700/60 rounded-xl overflow-hidden shadow-lg">
      {/* Table Toolbar */}
      <div className="p-4 border-b border-slate-700/60 flex flex-col md:flex-row gap-3 justify-between items-center">
        <div className="relative w-full md:w-80">
          <Search className="w-4 h-4 text-slate-400 absolute left-3 top-3" />
          <input
            type="text"
            data-testid="input-search"
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            placeholder="Search tests, status, or errors..."
            className="w-full bg-slate-900 border border-slate-700 rounded-lg pl-9 pr-3 py-2 text-sm text-slate-200 placeholder-slate-500 focus:outline-none focus:border-indigo-500"
          />
        </div>

        <div className="flex items-center gap-3 w-full md:w-auto">
          {/* Status Filter */}
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <Filter className="w-3.5 h-3.5" />
            <span>Status:</span>
            <select
              data-testid="select-status-filter"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-md px-2 py-1.5 focus:outline-none focus:border-indigo-500 cursor-pointer"
            >
              <option value="ALL">All Statuses</option>
              <option value="PASSED">Passed</option>
              <option value="FAILED">Failed</option>
            </select>
          </div>

          {/* Type Filter */}
          <div className="flex items-center gap-1.5 text-xs text-slate-400">
            <span>Type:</span>
            <select
              data-testid="select-type-filter"
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="bg-slate-900 border border-slate-700 text-slate-200 text-xs rounded-md px-2 py-1.5 focus:outline-none focus:border-indigo-500 cursor-pointer"
            >
              <option value="ALL">All Types</option>
              <option value="API">API Tests</option>
              <option value="UI">UI Tests</option>
            </select>
          </div>
        </div>
      </div>

      {/* Table Element */}
      <div className="overflow-x-auto">
        <table data-testid="results-table" className="w-full text-left border-collapse text-sm">
          <thead>
            <tr className="bg-slate-900/50 text-slate-400 border-b border-slate-700/60 text-xs font-semibold uppercase tracking-wider">
              <th className="py-3 px-4">Test Case Name</th>
              <th className="py-3 px-4">Type</th>
              <th className="py-3 px-4">Status</th>
              <th className="py-3 px-4">Duration</th>
              <th className="py-3 px-4">Executed At</th>
              <th className="py-3 px-4 text-right">Details</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-700/50">
            {loading ? (
              <tr>
                <td colSpan="6" className="py-8 text-center text-slate-400">
                  <div className="inline-flex items-center space-x-2">
                    <span className="w-4 h-4 border-2 border-indigo-500 border-t-transparent rounded-full animate-spin"></span>
                    <span>Loading test execution results...</span>
                  </div>
                </td>
              </tr>
            ) : filteredResults.length === 0 ? (
              <tr>
                <td colSpan="6" data-testid="results-empty-state" className="py-10 text-center text-slate-400">
                  <p className="text-base font-medium">No test results found</p>
                  <p className="text-xs text-slate-500 mt-1">
                    Try adjusting search filters or click "Run Tests" to execute a suite.
                  </p>
                </td>
              </tr>
            ) : (
              filteredResults.map((res) => {
                const isPassed = res.status === 'PASSED';
                const isExpanded = expandedRow === res.id;

                return (
                  <React.Fragment key={res.id}>
                    <tr
                      data-testid="result-row"
                      className="hover:bg-slate-700/30 transition-colors cursor-pointer"
                      onClick={() => toggleRow(res.id)}
                    >
                      <td className="py-3 px-4 font-medium text-white flex items-center gap-2">
                        {isPassed ? (
                          <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />
                        ) : (
                          <XCircle className="w-4 h-4 text-rose-400 shrink-0" />
                        )}
                        <span>{res.test_case_name}</span>
                      </td>

                      <td className="py-3 px-4">
                        <span
                          className={`text-xs px-2 py-0.5 rounded font-mono font-medium ${
                            res.test_type === 'API'
                              ? 'bg-blue-500/10 text-blue-400 border border-blue-500/20'
                              : 'bg-purple-500/10 text-purple-400 border border-purple-500/20'
                          }`}
                        >
                          {res.test_type || 'API'}
                        </span>
                      </td>

                      <td className="py-3 px-4">
                        <span
                          className={`text-xs px-2 py-0.5 rounded-full font-semibold ${
                            isPassed
                              ? 'bg-emerald-500/10 text-emerald-400 border border-emerald-500/20'
                              : 'bg-rose-500/10 text-rose-400 border border-rose-500/20'
                          }`}
                        >
                          {res.status}
                        </span>
                      </td>

                      <td className="py-3 px-4 text-slate-300 font-mono text-xs">
                        <div className="flex items-center gap-1">
                          <Clock className="w-3.5 h-3.5 text-slate-400" />
                          <span>{res.duration ? `${res.duration}s` : '< 0.01s'}</span>
                        </div>
                      </td>

                      <td className="py-3 px-4 text-slate-400 text-xs">
                        {res.executed_at ? new Date(res.executed_at).toLocaleTimeString() : 'N/A'}
                      </td>

                      <td className="py-3 px-4 text-right">
                        <button className="text-slate-400 hover:text-white p-1">
                          {isExpanded ? (
                            <ChevronUp className="w-4 h-4" />
                          ) : (
                            <ChevronDown className="w-4 h-4" />
                          )}
                        </button>
                      </td>
                    </tr>

                    {/* Expandable Error/Trace Drawer */}
                    {isExpanded && (
                      <tr className="bg-slate-900/70">
                        <td colSpan="6" className="p-4 text-xs">
                          <div className="space-y-2">
                            <div className="flex items-center gap-2 text-slate-300">
                              <span className="font-semibold text-slate-400">Run ID:</span>
                              <span className="font-mono">#{res.test_run_id}</span>
                              <span className="text-slate-600">|</span>
                              <span className="font-semibold text-slate-400">Case ID:</span>
                              <span className="font-mono">#{res.test_case_id}</span>
                            </div>

                            {res.error_message ? (
                              <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-800/50 text-rose-300 font-mono">
                                <div className="flex items-center gap-2 mb-1 text-rose-400 font-semibold">
                                  <AlertTriangle className="w-4 h-4" />
                                  <span>Failure Assertion Trace:</span>
                                </div>
                                <pre className="whitespace-pre-wrap">{res.error_message}</pre>
                              </div>
                            ) : (
                              <p className="text-emerald-400 font-medium flex items-center gap-1">
                                <CheckCircle2 className="w-3.5 h-3.5" />
                                All assertions validated successfully without errors.
                              </p>
                            )}
                          </div>
                        </td>
                      </tr>
                    )}
                  </React.Fragment>
                );
              })
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
