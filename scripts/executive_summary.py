#!/usr/bin/env python3
"""
executive_summary.py

Reads daily_report.txt, produced by scripts/log_analyser.py (Week 7 lab),
extracts the key backup health metrics, and writes a formatted
executive_summary.txt suitable for a non-technical audience (e.g. the
CBN compliance officer).

Input report format (written by log_analyser.py's write_report()):

    ==================================================
      Interswitch Daily Backup Health Report
      Date   : 2024-01-10
      Status : RED
    ==================================================

    --- Backup Summary ---
      Successful backups : 3
      Warnings            : 1
      Errors              : 1
    ...

Usage:
    python3 executive_summary.py
"""

import re
from datetime import datetime

# Same directory log_analyser.py writes its report to.
INPUT_FILE = "/tmp/interswitch_backups/daily_report.txt"
OUTPUT_FILE = "/tmp/interswitch_backups/executive_summary.txt"


# ---------------------------------------------------------------------------
# Part A: Read and Parse the Report
# ---------------------------------------------------------------------------
def read_report(filepath):
    """
    Open daily_report.txt, extract the report date, total backup count,
    success count, error count, and health status.

    Returns a tuple: (report_date, total_backups, success_count,
    error_count, health_status)

    Raises FileNotFoundError if the report does not exist (caller handles it).
    Raises ValueError if the report exists but a field cannot be found.
    """
    with open(filepath, "r") as f:
        contents = f.read()

    # log_analyser.py writes "Label : value" lines with varying amounts of
    # padding before the colon, so \s* around the colon covers that.
    date_match = re.search(r"Date\s*:\s*(\S+)", contents)
    status_match = re.search(r"Status\s*:\s*(GREEN|AMBER|RED)", contents, re.IGNORECASE)
    success_match = re.search(r"Successful backups\s*:\s*(\d+)", contents, re.IGNORECASE)
    error_match = re.search(r"Errors\s*:\s*(\d+)", contents, re.IGNORECASE)

    if not all([date_match, status_match, success_match, error_match]):
        raise ValueError(
            "daily_report.txt was found but is missing one or more expected "
            "fields (Date, Status, Successful backups, Errors). Check that "
            "log_analyser.py generated it correctly."
        )

    report_date = date_match.group(1)
    health_status = status_match.group(1).upper()
    success_count = int(success_match.group(1))
    error_count = int(error_match.group(1))
    # log_analyser.py doesn't print an explicit "Total Backups" line -
    # every directory it attempts ends up counted as SUCCESS or ERROR.
    total_backups = success_count + error_count

    return report_date, total_backups, success_count, error_count, health_status


# ---------------------------------------------------------------------------
# Part B: Build the Summary Using Lists and Dictionaries
# ---------------------------------------------------------------------------
def build_summary(report_date, total_backups, success_count, error_count, health_status):
    """
    Build the summary dictionary and the recommendations list.

    Returns a tuple: (summary, recommendations)
    """
    summary = {
        "report_date": report_date,
        "total_backups": total_backups,
        "success_count": success_count,
        "error_count": error_count,
        "health_status": health_status,
    }

    recommendations = []

    if health_status == "RED":
        recommendations.append(
            "URGENT: Investigate failed backup jobs immediately to prevent data loss."
        )
        recommendations.append(
            "URGENT: Escalate to the on-call engineer and review system logs for root cause."
        )
    elif health_status == "AMBER":
        recommendations.append(
            "Monitor upcoming backup runs closely to confirm the issue does not worsen."
        )
    elif health_status == "GREEN":
        recommendations.append(
            "No action needed. All backups completed successfully."
        )
    else:
        recommendations.append(
            "Health status unrecognized. Manually verify backup logs."
        )

    return summary, recommendations


# ---------------------------------------------------------------------------
# Part C: Write the Executive Summary to a File
# ---------------------------------------------------------------------------
def write_summary(summary, recommendations, output_path):
    """
    Write the formatted executive summary to output_path.
    """
    generated_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    description = (
        f"On {summary['report_date']}, the backup system processed "
        f"{summary['total_backups']} backup job(s), of which "
        f"{summary['success_count']} completed successfully and "
        f"{summary['error_count']} failed. The overall health status for "
        f"the day is rated {summary['health_status']}."
    )

    lines = []
    lines.append("EXECUTIVE SUMMARY - DAILY BACKUP HEALTH")
    lines.append("=" * 40)
    lines.append(f"Date: {summary['report_date']}")
    lines.append("")
    lines.append("Overview:")
    lines.append(description)
    lines.append("")
    lines.append("Recommendations:")
    for item in recommendations:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("-" * 40)
    lines.append(f"Generated by executive_summary.py on {generated_at}")

    with open(output_path, "w") as f:
        f.write("\n".join(lines) + "\n")


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    try:
        report_date, total_backups, success_count, error_count, health_status = (
            read_report(INPUT_FILE)
        )
    except FileNotFoundError:
        print(f"Error: '{INPUT_FILE}' was not found. Run scripts/log_analyser.py first.")
        return
    except ValueError as e:
        print(f"Error: {e}")
        return

    summary, recommendations = build_summary(
        report_date, total_backups, success_count, error_count, health_status
    )
    write_summary(summary, recommendations, OUTPUT_FILE)

    print(f"Executive summary written successfully to '{OUTPUT_FILE}'.")


if __name__ == "__main__":
    main()
