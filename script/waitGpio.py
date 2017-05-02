#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
  Send request to Jarvis when a specific GPIO changed its state
"""
__author__ = 'Quentin Comte-Gaz'
__email__ = "quentin@comte-gaz.com"
__license__ = "MIT License"
__copyright__ = "Copyright Quentin Comte-Gaz (2017)"
__python_version__ = "2.7+ and 3.+"
__version__ = "1.0 (2017/05/02)"
__status__ = "Usable for any project"
__dependency__ = "RPi.GPIO (use 'pip install RPi.GPIO' to install package)"

import RPi.GPIO as GPIO # RPI GPIO library
import time # Sleep
import argparse # Manage program arguments
import sys # Use exit calls
import logging # Add logging
import signal # Catch kill
import json # Read json input
import os # Build path
from subprocess import check_output # Run shell commands

class JarvisGpioServer():
  def __init__(self, gpio, pullUp, edgeDetectionEvent, phrase, mute=True, verbose=False):
    logging.debug("Initializing GPIO {} server.".format(str(gpio)))

    # Store variables
    self.mute_mode = mute
    self.verbose_mode = verbose
    self.gpio = gpio
    self.phrase = phrase

    # Show warnings if in debug mode
    GPIO.setwarnings(verbose)

    # Define the command line base to communicate with Jarvis with JSON
    self.program = [os.path.join(".", "jarvis.sh"), "-j"]

    # Set GPIO mode to use "Board PIN number" as reference
    GPIO.setmode(GPIO.BOARD)

    # Setup GPIO mode
    logging.debug("Setting IN mode to PIN {} with pull-up/down mode.".format(str(args.gpio)))
    GPIO.setup(args.gpio, GPIO.IN, pull_up_down=pullUp)

    # Add event detection for the GPIO PIN
    logging.debug("Adding event detection to callback function for PIN {}.".format(str(args.gpio)))
    GPIO.add_event_detect(gpio, edgeDetectionEvent)
    GPIO.add_event_callback(gpio, self.executeGpioOrder)

  def _exec(self, args):
    # Send command to Jarvis
    flags = []
    if self.mute_mode:
      flags.append(str("-m"))
    if self.verbose_mode:
      flags.append(str("-v"))
    command = self.program + flags + args
    logging.debug("Sending command '{}' to Jarvis.".format(str(command)))
    return check_output(command)

  def _executeOrder(self, phrase):
    # Say something to Jarvis
    return list(json.loads(self._exec([str("-x"), str(phrase)]).decode('utf-8'), strict=False))

  def executeGpioOrder(self, gpio):
    logging.debug("PIN {} edge change detected".format(str(gpio)))
    if gpio != self.gpio:
      logging.error("Wrong GPIO detected ({} instead of {})".format(str(gpio), str(self.gpio)))
      return False

    # Send request to Jarvis and receive answer
    response = self._executeOrder(str(self.phrase))
    logging.debug("Response from Jarvis: '{}'.".format(str(response)))
    return True

  def waitForever(self):
    logging.debug("Waiting PIN {} event detection...".format(str(self.gpio)))
    while True:
      time.sleep(100000)

  def properExit(self, signum, frame):
    # Exit the script properly
    logging.debug("Stopping GPIO edge detection event script.")
    # Clean all GPIO changes made by this script...
    GPIO.cleanup()
    # ... and exit this script without error (normal exit of the program)
    sys.exit(0)


if __name__ == "__main__":
  # Parse received parameters
  parser = argparse.ArgumentParser(description='Send request to Jarvis when a specific GPIO changed its state.')
  parser.add_argument('-g', '--gpio', type=int, help='GPIO pin (BOARD numbering system)')
  parser.add_argument('-r', '--request', help='Request to send to Jarvis (example: "Hello World")')
  parser.add_argument('-p', '--pullUp', default="DOWN", help='Pull-up/down mode (UP/DOWN, default: DOWN)')
  parser.add_argument('-e', '--edgeDetectionEvent', default="RISING", help='Edge detection events (RISING/FALLING/BOTH, default: RISING)')
  parser.add_argument('-v', '--verbose', action='store_true', help='Show debug information (optional, default: Not verbose)')
  parser.add_argument('-m', '--mute', action='store_true', help='Mute Jarvis (default: Not muted)')
  args = parser.parse_args()

  # Show more information if in debug mode
  if args.verbose:
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

  # Throw error in case the arguments are not valid
  if not args.gpio:
    logging.error("No GPIO pin specified.")
    sys.exit(1)
  if (args.request == ""):
    logging.error("Jarvis request must be specified.")
    sys.exit(1)
  if (args.pullUp != "DOWN") and (args.pullUp != "UP"):
    logging.error("Pull up/down mode must be 'UP' or 'DOWN'.")
    sys.exit(1)
  if (args.edgeDetectionEvent != "RISING") and (args.edgeDetectionEvent != "FALLING") and (args.edgeDetectionEvent != "BOTH"):
    logging.error("Edge detection event must be 'RISING' or 'FALLING' or 'BOTH'.")
    sys.exit(1)

  # Prepare to initialize the GPIO server class
  pull_up_mode = GPIO.PUD_DOWN
  if args.pullUp == "UP":
    pull_up_mode = GPIO.PUD_UP

  event_type = GPIO.BOTH
  if args.edgeDetectionEvent == "FALLING":
    event_type = GPIO.FALLING
  elif args.edgeDetectionEvent == "RISING":
    event_type = GPIO.RISING

  # Create a GPIO server instance
  gpio_server = JarvisGpioServer(gpio = args.gpio,
                                 pullUp = pull_up_mode,
                                 edgeDetectionEvent = event_type,
                                 phrase = args.request,
                                 mute = args.mute,
                                 verbose = args.verbose)

  # Add signals catching to quit application when jarvis ends
  for sig in [signal.SIGTERM, signal.SIGINT, signal.SIGHUP, signal.SIGQUIT]:
    signal.signal(sig, gpio_server.properExit)

  # Wait for a edge detection event forever
  gpio_server.waitForever()

  # Quit the program with error (the program should never go there)
  sys.exit(2)
