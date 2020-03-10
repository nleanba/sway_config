#! /usr/bin/fish

swayidle -w \
  timeout 0 'swaylock -C ~/.config/sway/swaylock.config' \
  timeout 0 'swaymsg "output * dpms off"' \
  resume    'swaymsg "output * dpms on"' \
  before-sleep 'swaylock -C ~/.config/sway/swaylock.config'