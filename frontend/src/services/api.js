import axios from 'axios';

// Create configured Axios instance
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000',
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

export const api = {
  // System Health
  async getHealth() {
    const res = await apiClient.get('/health');
    return res.data;
  },

  // Aggregated KPIs
  async getStats() {
    const res = await apiClient.get('/api/stats');
    return res.data;
  },

  // Test Case Definitions
  async getTestCases(testType = null) {
    const params = testType ? { test_type: testType } : {};
    const res = await apiClient.get('/api/tests', { params });
    return res.data;
  },

  async createTestCase(payload) {
    const res = await apiClient.post('/api/tests', payload);
    return res.data;
  },

  // Historical Test Runs
  async getRuns(limit = 20) {
    const res = await apiClient.get('/api/runs', { params: { limit } });
    return res.data;
  },

  async getRunById(runId) {
    const res = await apiClient.get(`/api/runs/${runId}`);
    return res.data;
  },

  // Test Results
  async getResults(filters = {}) {
    const res = await apiClient.get('/api/results', { params: filters });
    return res.data;
  },

  // Trigger Suite Execution
  async triggerTestRun(testType = 'ALL') {
    const res = await apiClient.post('/api/runs', { test_type: testType });
    return res.data;
  }
};

export default api;
