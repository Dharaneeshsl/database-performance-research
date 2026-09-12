"""
MongoDB Explain Plan Diagnostic Collector
Captures executionStats, totalDocsExamined, totalKeysExamined, nReturned, and winning plan stage.
"""

def analyze_mongo_query(db, collection_name: str, query_filter: dict):
    """Parses MongoDB explain('executionStats') dictionary."""
    col = db[collection_name]
    exp = col.find(query_filter).explain("executionStats")
    exec_stats = exp.get("executionStats", {})
    winning_plan = exp.get("queryPlanner", {}).get("winningPlan", {})

    stage = winning_plan.get("stage", "UNKNOWN")
    if stage == "FETCH" and "inputStage" in winning_plan:
        sub_stage = winning_plan["inputStage"].get("stage", "")
        stage = f"FETCH -> {sub_stage}"

    return {
        "executionTimeMillis": exec_stats.get("executionTimeMillis", 0),
        "totalDocsExamined": exec_stats.get("totalDocsExamined", 0),
        "totalKeysExamined": exec_stats.get("totalKeysExamined", 0),
        "nReturned": exec_stats.get("nReturned", 0),
        "plan_stage": stage
    }
