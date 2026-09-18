import os
import re

import mysql.connector
from flask import Flask, jsonify, request
--
app = Flask(__name__)
NAME = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*$")


def sql_name(value):
	if not NAME.fullmatch(value):
		raise ValueError("Invalid table or column name")
	return f"`{value}`"


def connect():
	return mysql.connector.connect(
		host=os.getenv("MYSQL_HOST", "localhost"),
		port=int(os.getenv("MYSQL_PORT", "3306")),
		user=os.getenv("MYSQL_USER", "root"),
		password=os.getenv("MYSQL_PASSWORD", ""),
		database=os.environ["MYSQL_DATABASE"],
	)


def json_rows(cursor, status=200):
	return jsonify(cursor.fetchall()), status


def close(connection, cursor):
	if cursor:
		cursor.close()
	if connection and connection.is_connected():
		connection.close()


@app.route("/records/<table>", methods=["GET", "POST"])
def records(table):
	connection = cursor = None
	try:
		table = sql_name(table)
		connection = connect()
		cursor = connection.cursor(dictionary=True)
		if request.method == "GET":
			filters = request.args.to_dict()
			where = " AND ".join(f"{sql_name(k)} = %s" for k in filters)
			query = f"SELECT * FROM {table}" + (f" WHERE {where}" if where else "")
			cursor.execute(query, list(filters.values()))
			return json_rows(cursor)

		data = request.get_json(silent=True)
		if not isinstance(data, dict) or not data:
			return jsonify(error="Body must be a non-empty JSON object"), 400
		columns = list(data)
		names = ", ".join(sql_name(c) for c in columns)
		marks = ", ".join(["%s"] * len(columns))
		cursor.execute(f"INSERT INTO {table} ({names}) VALUES ({marks})", [data[c] for c in columns])
		if cursor.rowcount != 1:
			connection.rollback()
			return jsonify(error="Write must affect exactly one row"), 409
		connection.commit()
		cursor.execute(f"SELECT * FROM {table} WHERE `id` = %s", (cursor.lastrowid,))
		return json_rows(cursor, 201)
	except (KeyError, ValueError, mysql.connector.Error) as error:
		if connection:
			connection.rollback()
		return jsonify(error=str(error)), 400
	finally:
		close(connection, cursor)


@app.route("/records/<table>/<int:record_id>", methods=["GET", "PUT", "DELETE"])
def record(table, record_id):
	connection = cursor = None
	try:
		table = sql_name(table)
		connection = connect()
		cursor = connection.cursor(dictionary=True)
		if request.method == "GET":
			cursor.execute(f"SELECT * FROM {table} WHERE `id` = %s", (record_id,))
			return json_rows(cursor)
		if request.method == "DELETE":
			cursor.execute(f"DELETE FROM {table} WHERE `id` = %s", (record_id,))
		else:
			data = request.get_json(silent=True)
			if not isinstance(data, dict) or not data:
				return jsonify(error="Body must be a non-empty JSON object"), 400
			assignments = ", ".join(f"{sql_name(c)} = %s" for c in data)
			cursor.execute(f"UPDATE {table} SET {assignments} WHERE `id` = %s", list(data.values()) + [record_id])
		if cursor.rowcount != 1:
			connection.rollback()
			return jsonify(error="Write must affect exactly one row"), 409
		connection.commit()
		cursor.execute(f"SELECT * FROM {table} WHERE `id` = %s", (record_id,))
		return json_rows(cursor)
	except (ValueError, mysql.connector.Error) as error:
		if connection:
			connection.rollback()
		return jsonify(error=str(error)), 400
	finally:
		close(connection, cursor)


if __name__ == "__main__":
	app.run(host="0.0.0.0", port=int(os.getenv("PORT", "5000")))
