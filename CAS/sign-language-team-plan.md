# Sign Language Translator — Team of 6 Task Distribution

**Challenge:** Edge AI & IoT for Resilient Smart Infrastructure (TSYP14, CAS + CRFID)
**Hardware:** NVIDIA Jetson + Raspberry Pi, **both doing the same task (sign → text/voice)**
**Deadlines:** Phase 1 (report + video) **20/11/2026** · Final (live demo + pitch) **09/12/2026**
**Plan date:** 05/10/2026 (about 6.5 weeks to Phase 1)

> ⚠️ **Team-size rule.** The challenge poster says **maximum 3 members per team**. Check with the organiser (wassim.jmal@ieee.org) whether 6 people can contribute while 3 are registered. The other option is to split into two registered teams with two different projects.

---

## 1. Concept: one translator, two edge versions

Both devices run the **same pipeline** and translate sign language into text and speech on their own. The only difference is the model:

| | **Jetson version** | **Raspberry Pi version** |
|---|---|---|
| Role | High-accuracy version | Low-cost, portable, low-power version |
| Model | Full model (e.g. Transformer / larger GRU, hands + pose + face keypoints) | Lightweight model (small GRU / 1D-CNN, hands-only keypoints, distilled from the big model) |
| Runtime | ONNX → **TensorRT FP16** on the GPU | **TFLite INT8** (or ONNX Runtime) on the CPU |
| Vocabulary | Full set (e.g. 30–50 signs) | Same set, or a reduced core set if accuracy drops |
| Target | Best accuracy, ~25+ FPS | Acceptable accuracy, real-time (≥ 10–15 FPS), cheap |

```
 Camera ─► Keypoint extraction ─► Sequence model ─► Smoothing + sentence builder ─► Screen subtitles + TTS voice
             (MediaPipe)          [Jetson: big model / TensorRT]
                                  [Pi:     light model / TFLite INT8]
```

**Story for the jury:** *"The same edge AI scales from a powerful device to a ~€80 one."* You show the trade-off between accuracy, speed, power and cost with real measurements. That covers the scoring for edge AI integration, innovation and deployment potential.

**CRFID point (1 pt):** both devices have an NFC reader. A user taps a card to load a profile: sign language (Tunisian SL / ASL), voice language (Arabic / French / English) and personal signs.

### Key engineering rule: shared code, swappable model
Write the application **once** and run it on both devices. Only the inference backend changes:

```python
class SignModel:            # common interface
    def predict(self, keypoint_window) -> (label, confidence): ...

class TensorRTModel(SignModel): ...   # Jetson
class TFLiteModel(SignModel): ...     # Raspberry Pi
```

Both versions must use the same label file, the same keypoint preprocessing and the same window size. Freeze these in week 1.

---

## 2. The 6 roles

### Role 1 — Team lead, integration and benchmarking
- Owns the repo, the shared application structure, the `SignModel` interface and the weekly schedule
- Runs the **Jetson vs Pi benchmark** on the same test set: accuracy, latency, FPS, power (USB power meter), cost. This is your strongest report and Q&A material.
- Final editor of the **4-page report**, and enforces **anonymity** (no names or logos anywhere, including on the devices)
- **Deliverables:** repo + README, benchmark table, final report

### Role 2 — Dataset and data collection
- Picks the vocabulary: **20–30 useful signs** for the MVP (greetings, yes/no, help, doctor, water, thanks, numbers…), extended later
- Builds the recording tool and runs recording sessions: several signers, lighting conditions, backgrounds and distances. Records with **both** cameras (the Pi camera and the Jetson camera), so both models see realistic input.
- Target: **≥ 40 clips per sign** from **≥ 4 signers**. Get consent from every signer.
- Can bootstrap from public datasets (WLASL, MS-ASL) and contact a local deaf association to validate Tunisian signs
- **Deliverables:** labelled dataset, train/val/test split by *signer* (so models are tested on unseen people)

### Role 3 — Main AI model (Jetson model)
- Keypoint pipeline + the **large model** (Transformer or bigger GRU, full keypoints)
- Augmentation (mirroring, scaling, temporal jitter), an "idle / unknown" class, a confidence threshold
- Evaluation: accuracy, confusion matrix, per-signer results
- Exports to ONNX and acts as the **teacher model** for Role 4
- **Deliverables:** big model v1 (week 3) and v2 (week 5), evaluation notebook

### Role 4 — Lightweight AI model (Raspberry Pi model)
- Designs the **small model**: fewer keypoints (hands only), smaller layers, shorter window
- **Knowledge distillation** from Role 3's model, then **INT8 quantization** to TFLite
- Measures the accuracy lost at each step (full → small → distilled → quantized). This is great material for the report.
- Tests whether the lighter MediaPipe settings (model complexity 0) are enough on the Pi
- **Deliverables:** small model v1 / v2 (`.tflite`), the step-by-step accuracy-loss table

### Role 5 — Jetson deployment
- Flashes JetPack and sets up the camera pipeline (GStreamer / OpenCV), with keypoint extraction running in real time
- Converts ONNX → **TensorRT FP16** and implements `TensorRTModel`
- Profiles and optimises FPS and latency. Sets up auto-start on boot (systemd), so the demo runs without a laptop.
- **Deliverables:** real-time Jetson translator, Jetson benchmark numbers

### Role 6 — Raspberry Pi deployment + hardware
- Sets up the Pi OS, the camera and the lightweight runtime (TFLite / ONNX Runtime), and implements `TFLiteModel`
- Makes the Pi reach real time: threading (camera / keypoints / model in separate threads), lower resolution, frame skipping
- Hardware for **both** devices: screen, speaker (offline TTS such as Piper / eSpeak-NG), NFC reader (RC522 / PN532), power, enclosures (**no logos**)
- Owns the **Phase 1 video** (both devices translating side by side)
- **Deliverables:** real-time Pi translator, assembled prototypes, demo video

> The shared app layer (smoothing, sentence builder, subtitles, TTS, NFC profiles) is written once. Role 1 owns it, Role 6 helps on TTS/NFC, and Role 5 tests it on the Jetson.

### Pairing (backup coverage)

| Pair | Why |
|---|---|
| Role 3 ↔ Role 4 | Teacher / student models, same labels and preprocessing |
| Role 3 ↔ Role 5 | Big model → TensorRT |
| Role 4 ↔ Role 6 | Small model → Pi runtime |
| Role 5 ↔ Role 6 | Same app on two devices, shared bug fixes |
| Role 2 ↔ everyone | Everyone records data in week 2 |

---

## 3. Timeline

| Week | Dates | Goals | Main owners |
|---|---|---|---|
| **W1** | 05–11 Oct | Flash both devices, freeze vocabulary + label file + preprocessing + `SignModel` interface, build recording tool, order parts (NFC, screens, speakers, Pi camera) | All, led by Role 1 |
| **W2** | 12–18 Oct | **Everyone records data.** Baseline model. Camera + MediaPipe running live on both devices. | 2, 3, 5, 6 |
| **W3** | 19–25 Oct | Big model v1 → TensorRT on the Jetson. Small model v1 → TFLite on the Pi. | 3, 4, 5, 6 |
| **W4** | 26 Oct–1 Nov | **Both devices translate end to end** (camera → text → voice), with the shared app and NFC profiles | 1 + all |
| **W5** | 2–8 Nov | Distillation + INT8 for the Pi, v2 models, full benchmark, enclosures, testing with new signers | 3, 4, 1, 6 |
| **W6** | 9–15 Nov | **Feature freeze.** Video (side-by-side demo), 4-page report | 1, 6 + all |
| **Buffer** | 16–20 Nov | Anonymity check, proofread, **submit Phase 1 (20/11)** | 1 |
| **Phase 2** | 21 Nov–9 Dec | Bigger vocabulary / sentences, demo hardening (lighting, boot time), 5-min pitch, Q&A rehearsal | All |

**Weekly rhythm:** a 30-minute sync each week where each person demos what works. Keep a running benchmark table in the repo.

---

## 4. Report sections, by owner (4 pages, anonymous)

| Section | Writer |
|---|---|
| Problem and impact (deaf community in Tunisia, communication barrier) | Role 2 |
| Solution and architecture (two edge versions, shared pipeline) | Role 1 |
| Intelligent processing: big model | Role 3 |
| Lightweight model: distillation + quantization | Role 4 |
| Edge deployment + benchmark (Jetson vs Pi) | Roles 5 + 6 + 1 |
| Innovation, CRFID/NFC, deployment potential | Role 1 |

## 5. Phase 2 pitch and Q&A
- **Presenters:** 2 speakers (suggested: Role 1 + Role 3); Roles 5 and 6 run the live demo on both devices
- **Q&A prep:** each role writes the 5 hardest questions about their own part, with answers. Likely questions:
  - "Why two devices doing the same thing?" → different use cases and budgets, and the measured trade-off
  - "How much accuracy did the Pi lose, and why?"
  - "How does it handle a new signer?"

## 6. Main risks

| Risk | Mitigation |
|---|---|
| The Pi is too slow (MediaPipe is the bottleneck, not the classifier) | Lower resolution, hands-only, MediaPipe complexity 0, frame skipping, threading. Try a Pi 5 if you have a Pi 4. |
| The small model's accuracy drops too much | Distillation, a reduced core vocabulary on the Pi, a higher confidence threshold |
| The two versions drift apart | One repo, one label file, one preprocessing module, the shared `SignModel` interface |
| Little public Tunisian SL data | Record your own data early (W2). Keep the vocabulary small and polished. |
| Live demo fails | Fixed lighting/background, a backup video ready |
| Team-size rule (max 3) | Confirm with the organiser this week |
