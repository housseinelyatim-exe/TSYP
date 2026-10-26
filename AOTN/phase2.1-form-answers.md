# AOTN Phase 2.1 — Form Answers

**Team name:** The Architects
**Student Branch:** IEEE ENSI SB

---

**What is your solution, and who is it for? (1-2 sentences)**

Nadhir is a low-cost box that uses a camera and a microphone to watch the existing dials, alarm lamps and siren of MT/BT transformer substations in Tunisian factories, and alerts the right people by SMS and voice call before a slow drift turns into a fire, without touching the certified installation. It is built for the on-call qualified electrician (habilité), with the night/weekend guard and the plant manager as secondary users.

**What are its 3 key features?**

1. Touch-nothing monitoring: the camera reads the existing dials and lamps and the microphone recognises the siren, so nothing is wired to the transformer and nothing needs re-certifying.
2. Two alert levels with trend detection: a slow drift raises WATCH (SMS to the electrician, with the time left before the limit); a limit reached, or two signals agreeing, raises INTERVENE NOW to the electrician and the guard at once.
3. Alerts that always reach a person: no acknowledgement in 5 minutes triggers a voice call and then escalation to the managers. A 2G backup on a second operator, a battery and a cloud watchdog keep alerts flowing if 4G or power fails, and every decision is logged to retune thresholds and cut false alarms.

**Which tools and technologies will you use to build it?**

An infrared night-vision camera and a USB microphone, connected to a Raspberry Pi class edge computer running Python. OpenCV reads the dial needles and lamps, and spectrum analysis detects the siren. A 4G modem is the main channel, with a 2G GSM module for backup SMS and voice calls. A UPS battery and the Pi's hardware watchdog keep the box running. In the cloud, PostgreSQL and a web dashboard handle readings, alerts and the decision log, with a heartbeat watchdog. Estimated prototype cost is about 800 TND.

**What is the biggest risk to your project, and how will you handle it?**

Misreading a dial or the siren (glare, darkness, factory noise), which would cause false alarms or missed ones. We handle it with a fixed mount with infrared light, a one-time calibration per dial, and a confidence score on every reading: when the score is low, Nadhir sends a "check needed" message instead of a false value. INTERVENE NOW also requires two signals to agree (dial plus lamp or siren). Every "false alarm" reply is used to recalibrate the site.

**Which need from your Phase 1 research does your solution answer best?**

The "last mile" from sensor to human. Our needs assessment and our interviews with technical directors and a technician showed that substations already detect the problem, but the alarm stays local and passive, so at night or on weekends nobody hears it and there is no fast way to intervene. Nadhir carries that existing warning to the electrician and the guard on site within seconds, and escalates until someone answers.

**Wrap-up (optional)**

Nadhir reflects a key Phase 1 interview finding: factories' existing maintenance software is too complex for floor and night staff, so it goes unused. The guard therefore needs no app, only an SMS answered with "1" or "2". The camera and microphone only observe, and no video leaves the site.
