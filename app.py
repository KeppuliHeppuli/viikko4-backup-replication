
import os
from flask import Flask
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    return mysql.connector.connect(
        host="127.0.0.1",
        user=os.environ["DB_USER"],
        password=os.environ["DB_PASSWORD"],
        database=os.environ["DB_NAME"]
    )

@app.route("/")
def home():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Read the counter without changing it
    cursor.execute("SELECT count FROM visits WHERE id = 1")
    result = cursor.fetchone()

    cursor.close()
    conn.close()

    visits = result[0] if result else 0
	#websitelayout
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>Week 4 - Database Replica</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background: #0f172a;
                color: white;
                margin: 0;
                padding: 40px 20px;
                text-align: center;
            }}
            .container {{
                max-width: 750px;
                margin: 60px auto;
                background: #1e293b;
                padding: 40px;
                border-radius: 15px;
            }}
            h1 {{ color: #60a5fa; }}
            .counter {{
                font-size: 64px;
                font-weight: bold;
                margin: 25px 0;
                color: #86efac;
            }}
            .info {{ color: #cbd5e1; }}
            .badge {{
                display: inline-block;
                background: #14532d;
                color: #86efac;
                padding: 10px 18px;
                border-radius: 20px;
                margin: 15px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>Week 4 - Database Replication</h1>
            <div class="badge">Read-Only Replica - Server B</div>

            <h2>Visitor Counter</h2>
            <div class="counter">{visits}</div>

            <p class="info">
                This counter is read from Server B's local MariaDB database.
            </p>
            <p class="info">
                refreshing this page doesn't increase the counter..
            </p>
<hr>

<h2>1. Server A and Server B</h2>

<p class="info">
    I use two Ubuntu servers in CSC cPouta.
    Server A is the original server, and Server B
    was created from a snapshot of Server A.
</p>

<p class="info">
    Server A: 195.148.20.149
</p>

<p class="info">
    Server B: 195.148.21.188
</p>

<p>
    <a href="http://195.148.20.149/viikko2/">
        Server A - Visitor Counter
    </a>
</p>

<hr>

<h2>2. Website Backups</h2>

<p class="info">
    I use rsync over SSH to copy website files
    from Server A to Server B.
</p>

<p class="info">
    Backups are saved in /srv/backups/server-a/
    with timestamps. Cron runs the script every hour.
</p>

<pre>0 * * * * /home/ubuntu/backup-scripts/backup.sh</pre>

<p class="info">
    I tested restoring a file from a backup.
    The SHA256 checksums matched the original.
</p>

<hr>

<h2>3. MariaDB Replication</h2>

<p class="info">
    Server A is the main database server,
    Server B is a read-only replica
</p>

<p class="info">
    MariaDB replicatoin runs through an SSH tunnel.
    Changes made on Server A are copied to Server B.
</p>

<p class="info">
    Server B only reads the visitor counter,
    Refreshing thispage doesn't increase it
</p>

<p class="info">
    Replication is not a backup because deleted
    data can also be deleted from the replica
</p>

<hr>

<h2>4. Users and Permissions</h2>

<p class="info">
    I use a separate MariaDB user for replication.
    The Flask app uses replica_reader, which only
    has SELECT permission.
</p>

<p class="info">
    SSH keys are used for backups and replication.
    Database passwords are stored in environment files.
</p>

<p class="info">
    Backup files are stored outside the public
    website folder with restricted permissions.
</p>

<hr>

<h2>5. Testing and Problems</h2>

<p class="info">
    I tested the visitor counter on both servers.
    Server B shows the updated count without increasing it.
</p>

<p class="info">
    I also tested restoring a backup file and rebooting
    Server B. Everything worked after the reboot.
</p>

<p class="info">
    One problem was getting the SSH connection to work
    automatically. I fixed it by creating a separate SSH key, this also created some issues when using a passphrase.  But i gave up on that and just created a SSH key without a passphrase. 
</p>

<p class="info">
    I also had to fix the MariaDB binary log position
    before replication started working.
</p>

        </div>
    </body>
    </html>
    """

@app.route("/api/health")
def health():
    return {"status": "healthy", "mode": "read-only"}
