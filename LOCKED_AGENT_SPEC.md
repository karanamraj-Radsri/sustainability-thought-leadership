# LOCKED AGENT SPECIFICATION

## Agent 1: trend_detector.py

### Complete Specifications:

**Data Flow:**  
1. Input: The agent receives streaming data from various sources (e.g., real-time market feeds, social media trends).
2. Processing: The agent analyzes incoming data for patterns and trends using predefined algorithms.
3. Output: The detected trends are then output for further evaluation or action.

**Output Formats:**  
- JSON: A structured format containing detected trends, e.g., `{ "trend": "rising", "confidence": 0.85 }`.
- CSV: A tabular format summarizing trends over time for external reporting.

**Scoring Criteria:**  
- **Precision:** The accuracy of detected trends versus actual observed events.
- **Recall:** The ability to capture all relevant trends within the data. 

**Execution Details:**  
- Frequency: Runs every 15 minutes to capture real-time data.
- Resource Allocation: Utilizes 4 CPU cores and 8GB RAM.

---  

## Agent 2: trend_curator.py

### Complete Specifications:

**Data Flow:**  
1. Input: Receives trends detected by `trend_detector.py`.
2. Processing: Curates trends by determining relevance and synthesizing actionable insights.
3. Output: Final curated trends are forwarded to decision-making systems or stakeholders.

**Output Formats:**  
- JSON: Contains curated insights, e.g., `{ "curated_trend": "market sentiment shifting towards eco-friendly products", "actionable": true }`.
- PDF: A summary report for stakeholders.

**Scoring Criteria:**  
- **Impact:** Evaluates how influential a curated trend can be on business strategies.
- **Timeliness:** Measures the speed of curation after trend detection.

**Execution Details:**  
- Frequency: Runs immediately after receiving input from `trend_detector.py`.
- Resource Allocation: Utilizes 2 CPU cores and 4GB RAM.
