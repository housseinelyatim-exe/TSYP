# Team 5, Person B: Timeline + logs

**People:** 1 · **Code:** `brain/src/timeline/` · **Read first:** [`00-overview-and-contracts.md`](00-overview-and-contracts.md), [`../city-brain-interface-spec.pdf`](../city-brain-interface-spec.pdf) sections 4, 8, 9 · **Partner:** Person A, safety + commands ([`05a-output-safety-commands.md`](05a-output-safety-commands.md))

## 1. Mission

You are the **voice of the City Brain**. You make everything the Brain does **visible**: live timeline screen and one log file per scenario (Phase 1 requirements R2 and R3).

## 2. You own / you don't own

| You own | You don't own |
|---|---|
| `brain/event` collection, timeline screen, log files, `/chain` display | Safety rules and commands (Person A) |
| Making sure every team publishes its events | Checking incoming messages (Input) |

## 3. Your inputs and outputs

| Direction | Topic | Content |
|---|---|---|
| In | `brain/event`, `brain/error` | Everything to show |
| In | Graph `GET /chain/{correlation_id}` | Full cause → effect chain |
| In (week 3) | Twin and Guardian timeline topics (e.g. `triplet/timeline/{layer}`) | Events of the other two layers |
| Out | Timeline screen, `logs/<scenario>-<time>.log` | What the jury sees |

## 4. Timeline screen

A web page (e.g. FastAPI + WebSocket, or a simple JS page subscribing to MQTT over WebSocket) showing a live list:

```
10:22:03.120  TWIN      water-level-04 = 2.4 m (port)
10:22:03.910  GUARDIAN  water-level-04: trusted
10:22:04.200  BRAIN     incident opened: flood at port (confidence 0.76)
10:22:05.900  BRAIN     LLM proposal: open valve-port-up 80%
10:22:05.950  BRAIN     decision: valve-port-up (score 1.53) over rules (1.21)
10:22:06.010  BRAIN     command sent → valve-port-up
10:22:06.400  TWIN      ack: valve-port-up open_80
```
- Colour per layer; refused actions and errors in red.
- Click an action → show its full chain (`/chain/{correlation_id}`).
- **Coordinate with the Twin and Guardian teams:** the timeline must show all three layers (R3). The Guardian team proposes `triplet/timeline/{layer}` topics; agree one format with them through the team lead.

## 5. Logs (R2)

- Every scenario run writes **one log file**: `logs/<scenario-id>-<YYYYMMDD-HHMMSS>.log`, JSON lines, all `brain/event` and `brain/error` messages.
- Must be readable by the jury after the event.

## 6. Events you must make sure exist

`incident_opened/updated/closed`, `llm_proposal`, `llm_timeout`, `decision`, `action_refused`, `command_sent`, `command_acknowledged`, `command_failed`, `guardian_offline`, `safe_mode_on/off`, `input_rejected`. Check with every team that they publish theirs. Event format: see `00-overview-and-contracts.md` section 3.

## 7. Tasks

### Week 1 (15–19 Oct)
- [ ] Event format frozen with all teams (**Fri 17 Oct**); first timeline page listing `brain/event`
- [ ] `config/safety.yaml` and outcome format (with Person A)

### Week 2 (20–26 Oct)
- [ ] Log file per scenario run; colours; refused / error display
- [ ] **Sun 26 Oct:** end-to-end run on mocks, visible on the timeline

### Week 3 (27 Oct – 2 Nov)
- [ ] Chain view; integrate Twin and Guardian events into the shared timeline
- [ ] Joint run: timeline on the big screen

### Week 4 (3–7 Nov)
- [ ] Report section: timeline and logs
- [ ] The timeline is the demo screen; prepare its layout for the projector

## 8. Done when

- [ ] Every scenario run produces exactly one log file
- [ ] The timeline shows a full flood chain from reading to ack in real time
- [ ] Scenarios B3, B4, B8: the refused action and its reason shown in red on the timeline
- [ ] Twin and Guardian events appear on the same timeline

## 9. Who you work with

| Who | About |
|---|---|
| **Person A (safety + commands)** | Events for refused / sent / acknowledged / failed commands |
| **Graph** | `/chain` endpoint |
| **All teams** | The events each must publish |
| **Team lead** | Shared timeline format with the Twin and Guardian teams |

## 10. Risks and tips

- The timeline is what the jury **looks at for 8 minutes**: make it readable from 5 metres.
- Don't let a missing `/chain` answer freeze the page: show the list even if the graph is down.
