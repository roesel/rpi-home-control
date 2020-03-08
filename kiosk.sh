#!/bin/bash

# Prevent blanking out of screen after inactivity
#xset s noblank
xset s off
xset -dpms

## Hide the mouse if it has been inactive for >5 s
#unclutter -idle 0.5 -root &
# Hide the mouse completely
unclutter -root &

# Search through the Chromium preferences file and clear out any flags that would make the warning bar appear
sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/pi/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/pi/.config/chromium/Default/Preferences

# Start chromium on a particular page
/usr/bin/chromium-browser --noerrdialogs --disable-infobars --disk-cache-dir=/dev/null --kiosk http://192.168.1.17/ --no-sandbox

#while true; do
#   xdotool keydown ctrl+Tab; xdotool keyup ctrl+Tab;
#   sleep 1
#done

