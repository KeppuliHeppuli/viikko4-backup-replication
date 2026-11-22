# Week 4 - Backups and Replication

This week, I used two Ubuntu servers in CSC cPouta. I created Server B from a snapshot of Server A.

## Backups

I made a Bash script that copies website files from Server A to Server B using rsync and SSH. Cron runs it every hour, and the backups are saved in folders with timestamps.

## Database Replication

I set up MariaDB replication between the servers using an SSH tunnel. Server B is read-only and shows the visitor counter from its own database.

## Testing

I tested the backups by restoring a file and comparing SHA256 checksums. I also checked that replication works and that the services start after rebooting Server B.

## Problems

I had some trouble with SSH keys and the MariaDB binary log position. After fixing those, everything started working.

## Links

- Server A: http://195.148.20.149/viikko2/
- Server B: http://195.148.21.188/viikko4/
