# Hab kurzerhand für dieses Smartmeter eine eigene MBus Hardware entwickelt
siehe https://inator.at/?p=1492

# Ausserdem
- script noch ein wenig angepasst, damit es auch funktioniert :-)
- und noch ein wenig erweitert :
  - kann jetzt direkt in eine MySQL schreiben (es wird aber dann JEDER Messwert geschrieben, d.h. so ca. alle 3 Sekunden)
  - kann auch direkt (in die RAMDisk) bei jedem neuen Messwert eine Datei überschreiben (damit man bei Auslieferung via Webserver möglichst aktuelle Daten sieht
  - Kann direkt ein Tasmota Gerät (z.B. umgeflashtes SonOff o.ä.) bei Überschuss ansteuern

# Inspiriert durch diesen Blog
https://www.michaelreitbauer.at/blog


# SmartMeterEVN
Dieses Projekt ermöglicht es den Smartmeter der EVN (Netz Niederösterreich) über die Kundenschnittstelle auszulesen.
Smart Meter werden von der Netz NÖ GmbH eingebaut, auf Basis der gesetzlichen Forderungen.

## Getting Started
### Voraussetzungen Hardware


* Passwort für die Kundenschnittstelle
  * Alle folgenden Informationen sind aus dem Folder der EVN. (https://www.netz-noe.at/Download-(1)/Smart-Meter/218_9_SmartMeter_Kundenschnittstelle_lektoriert_14.aspx)
  * Wenn bereits ein Smart Meter in der Kundenanlage eingebaut ist, kann hier das der Schlüssel angefordert werden: smartmeter@netz-noe.at
    * Kundennummer oder Vertragskontonummer
    * Zählernummer
    * Handynummer




### Zähler Hersteller
* Kaifa Drehstromzähler MA309


## License

This project is licensed under the GNU General Public License v3.0 License - see the LICENSE.md file for details
