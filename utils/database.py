import sqlite3
import os
import pandas as pd
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "database", "retinaguard.db")


def get_connection():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    return sqlite3.connect(DB_PATH, check_same_thread=False)


def init_database():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            filename TEXT NOT NULL,
            patient_id TEXT,
            age INTEGER,
            gender TEXT,
            exam_number TEXT,
            predicted_class TEXT NOT NULL,
            confidence REAL NOT NULL,
            severity TEXT,
            risk TEXT,
            clinical_note TEXT,
            recommendation TEXT,
            no_dr REAL,
            mild REAL,
            moderate REAL,
            severe REAL,
            proliferative REAL,
            quality_score TEXT,
            brightness REAL,
            contrast REAL,
            blur_score REAL,
            notes TEXT
        )
    """)
    conn.commit()
    conn.close()


def save_prediction(filename, predicted_class, confidence, probabilities,
                    patient_data=None, severity_info=None, clinical_note="",
                    recommendation="", quality_info=None):
    conn = get_connection()
    cursor = conn.cursor()

    probs = probabilities if probabilities else [0, 0, 0, 0, 0]
    q = quality_info or {}
    pd_data = patient_data or {}

    cursor.execute("""
        INSERT INTO predictions (
            timestamp, filename, patient_id, age, gender, exam_number,
            predicted_class, confidence, severity, risk, clinical_note, recommendation,
            no_dr, mild, moderate, severe, proliferative,
            quality_score, brightness, contrast, blur_score, notes
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        datetime.now().isoformat(),
        filename,
        pd_data.get("patient_id", ""),
        pd_data.get("age"),
        pd_data.get("gender", ""),
        pd_data.get("exam_number", ""),
        predicted_class,
        round(confidence, 4),
        (severity_info or {}).get("severity", ""),
        (severity_info or {}).get("risk", ""),
        clinical_note,
        recommendation,
        round(probs[0], 4),
        round(probs[1], 4),
        round(probs[2], 4),
        round(probs[3], 4),
        round(probs[4], 4),
        q.get("quality_score", "N/A"),
        round(q.get("brightness", 0), 2),
        round(q.get("contrast", 0), 2),
        round(q.get("blur_score", 0), 2),
        ""
    ))
    conn.commit()
    conn.close()


def get_all_predictions():
    conn = get_connection()
    try:
        df = pd.read_sql_query(
            "SELECT * FROM predictions ORDER BY timestamp DESC", conn
        )
    except Exception:
        df = pd.DataFrame()
    finally:
        conn.close()
    return df


def get_prediction_by_id(record_id):
    conn = get_connection()
    try:
        df = pd.read_sql_query(
            "SELECT * FROM predictions WHERE id = ?", conn, params=(record_id,)
        )
        if not df.empty:
            return df.iloc[0].to_dict()
        return None
    except Exception:
        return None
    finally:
        conn.close()


def delete_prediction(record_id):
    conn = get_connection()
    conn.execute("DELETE FROM predictions WHERE id = ?", (record_id,))
    conn.commit()
    conn.close()


def clear_all_predictions():
    conn = get_connection()
    conn.execute("DELETE FROM predictions")
    conn.commit()
    conn.close()


def get_stats():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM predictions")
    total = cursor.fetchone()[0]
    cursor.execute("SELECT predicted_class, COUNT(*) as cnt FROM predictions GROUP BY predicted_class")
    class_counts = dict(cursor.fetchall())
    cursor.execute("SELECT AVG(confidence) FROM predictions")
    avg_conf = cursor.fetchone()[0] or 0
    conn.close()
    return {"total": total, "class_counts": class_counts, "avg_confidence": avg_conf}
