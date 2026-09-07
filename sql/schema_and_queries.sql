-- =====================================================================
-- Database Schema and Analytical Queries
-- Study: Beyond Proficiency: Unpacking Cognitive Engagement with GenAI
-- Target DBMS: PostgreSQL / SQLite (Scalable Relational Architecture)
-- =====================================================================

-- Table 1: Participants (Demographics, Background & Baseline Measures)
CREATE TABLE IF NOT EXISTS participants (
    participant_id VARCHAR(20) PRIMARY KEY,
    gender VARCHAR(10),
    age INT,
    l1_language VARCHAR(50) DEFAULT 'Persian',
    target_language VARCHAR(50) DEFAULT 'English',
    proficiency_level VARCHAR(20) NOT NULL CHECK (proficiency_level IN ('Intermediate', 'Advanced')),
    oxford_quick_placement_score NUMERIC(5, 2),
    writing_score NUMERIC(5, 2) NOT NULL CHECK (writing_score >= 0 AND writing_score <= 20),
    genai_familiarity_years NUMERIC(3, 1),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Table 2: Cognitive Engagement Responses (Long/Item-Level Format)
CREATE TABLE IF NOT EXISTS cognitive_engagement_responses (
    response_id SERIAL PRIMARY KEY,
    participant_id VARCHAR(20) NOT NULL,
    stage VARCHAR(20) NOT NULL CHECK (stage IN ('Pre-writing', 'Drafting', 'Editing')),
    strand VARCHAR(20) NOT NULL CHECK (strand IN ('Linguistic', 'Strategic', 'Critical')),
    item_code VARCHAR(20) NOT NULL,
    score INT NOT NULL CHECK (score >= 1 AND score <= 6),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id) ON DELETE CASCADE
);

-- Table 3: Aggregate Stage & Strand Summary Metrics
CREATE TABLE IF NOT EXISTS participant_stage_metrics (
    metric_id SERIAL PRIMARY KEY,
    participant_id VARCHAR(20) NOT NULL,
    stage VARCHAR(20) NOT NULL,
    mean_engagement NUMERIC(4, 3) NOT NULL,
    linguistic_mean NUMERIC(4, 3),
    strategic_mean NUMERIC(4, 3),
    critical_mean NUMERIC(4, 3),
    FOREIGN KEY (participant_id) REFERENCES participants(participant_id) ON DELETE CASCADE
);

-- Indices for Optimized Analytical Queries
CREATE INDEX idx_stage_strand ON cognitive_engagement_responses (stage, strand);
CREATE INDEX idx_participant_stage ON participant_stage_metrics (participant_id, stage);

-- =====================================================================
-- ANALYTICAL QUERIES
-- =====================================================================

-- Query 1: Stage-by-Proficiency Interaction Aggregates
SELECT
    p.proficiency_level,
    r.stage,
    ROUND(AVG(r.score), 3) AS mean_cognitive_engagement,
    ROUND(STDDEV(r.score), 3) AS sd_engagement,
    COUNT(DISTINCT p.participant_id) AS n_participants
FROM participants p
JOIN cognitive_engagement_responses r ON p.participant_id = r.participant_id
GROUP BY p.proficiency_level, r.stage
ORDER BY r.stage, p.proficiency_level;

-- Query 2: Correlation View between Editing Engagement and Writing Score
SELECT
    p.participant_id,
    p.proficiency_level,
    p.writing_score,
    ROUND(AVG(r.score), 3) AS editing_engagement_mean
FROM participants p
JOIN cognitive_engagement_responses r ON p.participant_id = r.participant_id
WHERE r.stage = 'Editing'
GROUP BY p.participant_id, p.proficiency_level, p.writing_score
ORDER BY p.writing_score DESC;
