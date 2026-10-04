-- ==========================================================
-- TESTPILOT DATABASE SCHEMA
-- Target Database: MySQL 8.0+
-- Database Name: testpilot
-- ==========================================================

CREATE DATABASE IF NOT EXISTS testpilot;
USE testpilot;

-- Table 1: test_cases
-- Defines individual automated test definitions (API or Web UI)
DROP TABLE IF EXISTS test_results;
DROP TABLE IF EXISTS test_runs;
DROP TABLE IF EXISTS test_cases;

CREATE TABLE test_cases (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    test_type VARCHAR(50) NOT NULL, -- 'API' or 'UI'
    description TEXT,
    endpoint_or_url VARCHAR(500) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_test_type (test_type),
    INDEX idx_test_name (name)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 2: test_runs
-- Tracks entire test execution suite sessions
CREATE TABLE test_runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    started_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP NULL DEFAULT NULL,
    total_tests INT DEFAULT 0,
    passed_tests INT DEFAULT 0,
    failed_tests INT DEFAULT 0,
    status VARCHAR(50) DEFAULT 'RUNNING', -- 'RUNNING', 'COMPLETED', 'FAILED'
    INDEX idx_run_status (status),
    INDEX idx_run_started_at (started_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Table 3: test_results
-- Granular execution outcomes linking a specific test run to a test case
CREATE TABLE test_results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    test_run_id INT NOT NULL,
    test_case_id INT NOT NULL,
    status VARCHAR(50) NOT NULL, -- 'PASSED', 'FAILED', 'SKIPPED'
    duration FLOAT DEFAULT 0.0,  -- Execution duration in seconds
    error_message TEXT NULL,
    executed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_results_run FOREIGN KEY (test_run_id) 
        REFERENCES test_runs(id) ON DELETE CASCADE,
    CONSTRAINT fk_results_case FOREIGN KEY (test_case_id) 
        REFERENCES test_cases(id) ON DELETE CASCADE,
    INDEX idx_result_run (test_run_id),
    INDEX idx_result_case (test_case_id),
    INDEX idx_result_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
