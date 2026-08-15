#!/data/data/com.termux/files/usr/bin/bash
cd /data/data/com.termux/files/usr/share/nginx/html
pkill -f admin_server.py 2>/dev/null
sleep 1
nohup python3 admin_server.py > server.log 2>&1 &
sleep 2
echo "✅ السيرفر مشغل من جديد"
cat server.log | tail -5
