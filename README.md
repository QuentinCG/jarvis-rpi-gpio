## Description
Control Raspberry Pi GPIO with <a target="_blank" href="http://domotiquefacile.fr/jarvis/">Jarvis assistant</a>.

<img src="https://raw.githubusercontent.com/QuentinCG/jarvis-rpi-gpio/master/presentation.jpg" width="100">


## Usage
```
[Capteur PIR détecte un mouvement]
Jarvis: Je te vois.
```


In future release (not finished yet):

```
You: Active le GPIO x en pull-up
Jarvis: GPIO x activé

You: Désactive le GPIO x en pull-up
Jarvis: GPIO x désactivé

You: Donne l'état du GPIO x
Jarvis: Le GPIO x est à l'état bas.
```


## How to install

1) Add this plugin to your Jarvis assistant (<a target="_blank" href="http://domotiquefacile.fr/jarvis/content/plugins">more info here</a>): ```./jarvis.sh -p https://github.com/QuentinCG/jarvis-rpi-gpio```

2) Configure the <a target="_blank" href="https://github.com/QuentinCG/jarvis-rpi-gpio/blob/master/hooks/program_startup">program startup</a> to match your PIN and configuration (don't edit if you keep the PINOUT explained in this README).

3) Connect your PIR sensor to Raspberry PI as followed (or any other digital sensor):

PIR Sensor  | Raspberry Pi
-------- |  --------
VCC      | 5V
GND      | GND
D0       | PIN 15 (GPIO 22)

<img src="https://raw.githubusercontent.com/QuentinCG/jarvis-rpi-gpio/master/pinout.png" width="200">

4) Enjoy


## Author
[Quentin Comte-Gaz](http://quentin.comte-gaz.com/)


## License

This project is under MIT license. This means you can use it as you want (just don't delete the plugin header).


## Contribute

If you want to add more examples or improve the plugin, just create a pull request with proper commit message and right wrapping.
