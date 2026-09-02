#!/bin/bash
HEADER="User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
RESULTS_DIR="C:/Users/koda3/AetherHome/scripts/amazon_pages"
mkdir -p "$RESULTS_DIR"
ASINS=(
  "B0FJ8LWL7J|Philips Hue Bridge Pro"
  "B0FJY1PGK7|Hue Essential Starter Kit"
  "B07BVQZSGG|Hue White and Color Ambiance Starter Kit"
  "B0H2971ML4|Hue Play Floor Lamp"
  "B09CV7MT5S|Hue Outdoor Sensor"
  "B0C5P9QZQX|Ecobee Smart Thermostat Premium"
  "B07NQVWRR3|Ecobee SmartSensor 2-Pack"
  "B087D6DRCC|Ecobee SmartCamera"
  "B0BL21BY4Y|Arlo Pro 5S"
  "B0G6M1KKN3|Arlo Ultra 3"
  "B0CRVJ79LB|Arlo Video Doorbell 2K"
  "B08B3B3LQ3|Arlo Essential Spotlight Camera"
  "B08BG1DZKJ|Arlo Floodlight Camera"
  "B0BVDCGY9Y|August Connect"
  "B0CT8W9NRB|Aqara Motion Sensor P2"
  "B0FLXXF4YW|Aqara Hub M200"
  "B07D37VDM3|Aqara Door and Window Sensor"
  "B07D39MSZS|Aqara Water Leak Sensor"
  "B09Y5Q6Z29|Aqara Camera G3"
  "B0GHNCY7VZ|Roborock Qrevo S Pro"
)
for entry in "${ASINS[@]}"; do
  ASIN="${entry%%|*}"
  NAME="${entry##*|}"
  URL="https://www.amazon.co.uk/gp/product/${ASIN}"
  OUTFILE="${RESULTS_DIR}/${ASIN}.html"
  echo "Fetching $NAME ($ASIN)..."
  curl -s --compressed --max-time 30 -H "$HEADER" "$URL" -o "$OUTFILE"
  if grep -q "bm-verify" "$OUTFILE"; then
    echo "  Bot check for $ASIN"
  else
    echo "  Saved to $OUTFILE"
  fi
  sleep 3
done
