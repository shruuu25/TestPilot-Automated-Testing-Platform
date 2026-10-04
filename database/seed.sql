-- ==========================================================
-- TESTPILOT DATABASE SEED DATA
-- Target Database: testpilot
-- ==========================================================

USE testpilot;

-- Insert Base Test Cases (API & UI)
INSERT INTO test_cases (id, name, test_type, description, endpoint_or_url, created_at) VALUES
(1, 'Verify API Health Endpoint', 'API', 'Validates that GET /health returns HTTP 200 with operational status', '/health', NOW()),
(2, 'Get All Test Cases API', 'API', 'Validates that GET /api/tests returns array of registered test definitions', '/api/tests', NOW()),
(3, 'Create New Test Case API', 'API', 'Validates that POST /api/tests creates a valid test record with HTTP 201', '/api/tests', NOW()),
(4, 'Get Test Case By Valid ID', 'API', 'Validates fetching an individual test definition by primary key', '/api/tests/{id}', NOW()),
(5, 'Negative: Non-existent Test ID', 'API', 'Ensures GET /api/tests/999999 gracefully returns HTTP 404', '/api/tests/999999', NOW()),
(6, 'Negative: Invalid Test Case Payload', 'API', 'Ensures POST /api/tests with invalid payload returns HTTP 422', '/api/tests', NOW()),
(7, 'Dashboard KPI Metrics Render', 'UI', 'Verifies total test cases, total runs, and pass rate cards render correctly', 'http://localhost:5173/', NOW()),
(8, 'Test Results Table Render', 'UI', 'Verifies that the results table contains columns for Case, Type, Status, Duration', 'http://localhost:5173/', NOW()),
(9, 'Test Execution Trigger', 'UI', 'Verifies clicking the Run Tests button triggers suite execution and updates dashboard', 'http://localhost:5173/execute', NOW()),
(10, 'Status Filter Functionality', 'UI', 'Verifies filtering test results table by PASSED and FAILED states', 'http://localhost:5173/', NOW());

-- Insert Historical Test Runs
INSERT INTO test_runs (id, started_at, completed_at, total_tests, passed_tests, failed_tests, status) VALUES
(1, DATE_SUB(NOW(), INTERVAL 2 HOUR), DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE), 8, 8, 0, 'COMPLETED'),
(2, DATE_SUB(NOW(), INTERVAL 30 MINUTE), DATE_SUB(NOW(), INTERVAL 28 MINUTE), 10, 9, 1, 'COMPLETED');

-- Insert Test Results for Run 1 (All Passed)
INSERT INTO test_results (test_run_id, test_case_id, status, duration, error_message, executed_at) VALUES
(1, 1, 'PASSED', 0.045, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 59 MINUTE)),
(1, 2, 'PASSED', 0.082, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 59 MINUTE)),
(1, 3, 'PASSED', 0.112, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE)),
(1, 4, 'PASSED', 0.063, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE)),
(1, 5, 'PASSED', 0.038, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE)),
(1, 6, 'PASSED', 0.042, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE)),
(1, 7, 'PASSED', 1.250, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE)),
(1, 8, 'PASSED', 0.950, NULL, DATE_SUB(NOW(), INTERVAL 1 HOUR + INTERVAL 58 MINUTE));

-- Insert Test Results for Run 2 (9 Passed, 1 Failed)
INSERT INTO test_results (test_run_id, test_case_id, status, duration, error_message, executed_at) VALUES
(2, 1, 'PASSED', 0.039, NULL, DATE_SUB(NOW(), INTERVAL 30 MINUTE)),
(2, 2, 'PASSED', 0.071, NULL, DATE_SUB(NOW(), INTERVAL 30 MINUTE)),
(2, 3, 'PASSED', 0.104, NULL, DATE_SUB(NOW(), INTERVAL 29 MINUTE)),
(2, 4, 'PASSED', 0.055, NULL, DATE_SUB(NOW(), INTERVAL 29 MINUTE)),
(2, 5, 'PASSED', 0.035, NULL, DATE_SUB(NOW(), INTERVAL 29 MINUTE)),
(2, 6, 'PASSED', 0.041, NULL, DATE_SUB(NOW(), INTERVAL 29 MINUTE)),
(2, 7, 'PASSED', 1.180, NULL, DATE_SUB(NOW(), INTERVAL 29 MINUTE)),
(2, 8, 'PASSED', 0.890, NULL, DATE_SUB(NOW(), INTERVAL 28 MINUTE)),
(2, 9, 'PASSED', 1.450, NULL, DATE_SUB(NOW(), INTERVAL 28 MINUTE)),
(2, 10, 'FAILED', 0.620, 'AssertionError: Expected filter count to be 2, but received 0 matching rows within timeout of 5s', DATE_SUB(NOW(), INTERVAL 28 MINUTE));
