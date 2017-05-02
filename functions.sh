#!/usr/bin/env bash

# Execute Jarvis command every time a edge event is detected for a specific GPIO (asynchronous)
# $1 (int): PIN of the GPIO to check
# $2 (string): Pull up/down mode (UP/DOWN)
# $3 (string): Edge detection events (RISING/FALLING/BOTH)
# $4 (string): Request to send to Jarvis when a edge event is detected
# $5 (bool): Mute Jarvis response ("True" for Jarvis not answering with speakers, else "False")
# $6 (bool, optional): Verbose ("True" for showing debug info, "False" or no value for not showing debug info)
jv_pg_rg_asynch_edge_detect_gpio()
{
  jv_debug "Starting GPIO $1-Jarvis server PULL-$2: request '$4' will be sent to Jarvis when edge detection event $3 happens."

  # Start the server
  local dir="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

  local mute_arg=""
  if [ $5 = "True" ]; then
    mute_arg="--mute"
  fi

  local verbose_arg=""
  if [ $6 = "True" ]; then
    verbose_arg="--verbose"
    python $dir/script/waitGpio.py --gpio $1 --pullUp $2 --edgeDetectionEvent $3 --request "$4" $mute_arg $verbose_arg &
  else
    nohup python $dir/script/waitGpio.py --gpio $1 --pullUp $2 --edgeDetectionEvent $3 --request "$4" $mute_arg $verbose_arg >/dev/null 2>/dev/stdout &
  fi
}
