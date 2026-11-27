# data-swe: SWE tool-output trajectories for observation-likelihood scoring

These are non-terminal companions to `../../terminal/data` (AgenticPPL). They let the same scorer test "general tool responses": file views, edit acknowledgements, test runs, search results and script output. Built by `build.py`, CPU only, seed 0. Raw downloads are in `raw/` and can be deleted; `build.py` needs them to rebuild.

## Files

| file | trajectories | source (revision) | generator | tasks created | licence |
|---|---|---|---|---|---|
| `swe_smith.jsonl.gz` | 300 | `SWE-bench/SWE-smith-trajectories` @ `08e109b`, `tool` config, shard 0 | Claude 3.7 Sonnet, SWE-agent | synthetic bugs in existing repos, early 2025 | MIT |
| `swe_rebench.jsonl.gz` | 150 | `nebius/SWE-rebench-leaderboard-trajectories` @ `ed7fa38`, `python_spring2026` | Claude Opus 4.6, GPT-5.4, Gemini 3.1 Pro, GLM-5.1, DeepSeek-V4-Pro (30 each), `swelike-py` scaffold | **2026-03 to 2026-05** | CC-BY-4.0 |
| `swe_rebench_openhands.jsonl.gz` | 150 | `nebius/SWE-rebench-openhands-trajectories` @ `3545538`, dates joined from `nebius/SWE-rebench` @ `89cdfba` | Qwen3-Coder-480B-A35B or a Nebius fine-tune of it (per-row model not released), OpenHands v0.54 | 2024-10-01 to 2025-03-31 | CC-BY-4.0 |

`stats.json` holds the full statistics; the tables below summarise it.

### Evaluation dates
The OpenHands subset predates June 2025: every task in `nebius/SWE-rebench` (test plus filtered) was created on or before 2025-04-30.

The contamination-controlled set is therefore `swe_rebench.jsonl.gz`, taken from Nebius's leaderboard release. Its tasks were created March–May 2026, after the Qwen3 release (2025-04) and after Nemotron-Terminal. No teacher in it belongs to the Qwen family.

The OpenHands set is kept as a secondary set, using the most recent tasks available (2024-10 onward). It has two problems:
- **Self-family bias:** the generator is Qwen3-Coder, the same family as the scored Qwen3 and Nemotron models.
- **Possible pretraining exposure:** its tasks predate Qwen3's release. Qwen3's exact data cutoff is not public.

## Sampling
- **SWE-smith:** from shard 0 of the `tool` config (3,013 rows), keep Claude 3.7 Sonnet, `resolved`, one trajectory per instance. Then round-robin over the 115 repos in shuffled order until 300 are picked.
- **Leaderboard 2026:** keep `scaffold == swelike-py`, the 5 teachers above, and `resolved == 1`. For each (teacher, task) keep the shortest resolved run of the 5, so more trajectories fit a 32k-token window. Then take 30 tasks per teacher, least-used tasks first, to spread coverage over the 110 tasks. Result: 86 distinct tasks and 66 repos.
- **OpenHands:** keep tasks created on or after 2024-10-01 with `resolved == 1` and `exit_status == submit`, one trajectory per instance, then round-robin over repos (most recent first) until 150 are picked. This gives 150 tasks over 126 repos.

## Record schema
Records follow AgenticPPL's schema plus extra fields.

| field | meaning |
|---|---|
| `id` | sha256 of `text`, first 16 hex characters |
| `split`, `source`, `source_revision`, `source_ref`, `licence`, `task_id`, `repo`, `teacher`, `resolved`, `n_turns` | provenance |
| `task_month` | leaderboard set only |
| `task_created_at` | OpenHands set only |
| `messages` | `[{role, content, parts:[[type, turn, char_offset]], tool_result?}]`; tool results are `role: "user"` with `tool_result: true` (one message per tool result) |
| `text` | canonical rendering `<|user|>task<|assistant|>…<|user|>result…`; role tags fall in no span |
| `spans` | `[byte_start, byte_end, type, turn]` over the UTF-8 `text`; `type` is one of `task`, `thought`, `action`, `markup`, `observation`; turn −1 is the task |
| `observations` | one entry per tool result: `{byte_start, byte_end, turn, n_bytes, tool, command, obs_kind, error, error_regex_raw, exit_code, tests_pass, truncated, truncation_marker}`. On the leaderboard set, `status` is also recorded |

### Rendering rules
- **Assistant turn:** `thought` text, then for each call ``\n<tool_call>\n{"name": "<tool>", "arguments": `` (markup), the JSON-encoded arguments (`action`), and `}\n</tool_call>` (markup).
  - The action span is the whole argument object: the bash command, or the editor's `path`/`old_str`/`new_str`.
  - Leaderboard GPT-5.4 and Gemini trajectories contain no assistant text, so their turns are actions only.
- **The task** is the system prompt plus the first user prompt.
- **Scaffold wrappers become markup:**
  - SWE-smith's `OBSERVATION:\n` prefix;
  - OpenHands' trailing `[The command completed with exit code N.] [Current working directory …] [Python interpreter …]` footer;
  - leaderboard scaffold failures, where the agent's tool call could not be parsed or was not invoked. The text the agent saw for these is not released, so the stub `[scaffold error: <type>]` is markup and produces no observation entry.
- **Line endings:** `\r\n` is normalised to `\n`. ANSI colour codes are kept in the text and stripped only for labelling.

## Labelling rules

### `obs_kind`
The first matching rule wins. Commands are parsed after dropping heredoc bodies and quoted strings. Leading `cd`/`export`/`timeout`/`VAR=` words are skipped, and `echo`/`printf` segments are ignored.

1. **`tool_ack`:** bookkeeping tools (`think`, `task_tracker`, `finish`, `submit`), "Your thought has been logged", or a command made only of `echo`/`printf`. GPT-5.4 writes its notes this way.
   - *Note:* SWE-agent's `submit` result is a fixed review checklist plus the agent's own diff. It is copyable but large, about 17% of SWE-smith observation bytes.
2. **`edit_ack`:** editor mutations (`create`, `str_replace`, `insert`, `undo_edit`), SWE-agent `edit`/`replace`/`create` commands in any segment, or acknowledgement text such as "has been edited", "File created successfully" or "File updated. Please review". These often echo a `cat -n` snippet of the edited region.
3. **`search`, for directory listings:** an editor `view` of a directory ("files and directories up to 2 levels").
4. **`file_view`:** an editor `view`, SWE-agent `open`/`goto`/`scroll`, a "result of running `cat -n`" result, or a `[File: …]` result.
5. **`test_run`:** the command mentions pytest, py.test, unittest, tox, nox, `manage.py test`, `make test`/`check`, runtests, `cargo test`, `go test` or `npm test`. Also matches when the output contains "test session starts" or "Ran N tests".
6. **`search`:** grep/rg/ag/ack/find/fd/ls/tree/locate/which/`git grep` as the first program, or SWE-agent `search_*`/`find_file`.
7. **`python_exec`:** any segment runs `python*`, including `cat > t.py <<EOF … EOF; python t.py`.
8. **`file_view` via shell:** the first program is cat/head/tail/nl/less/more/bat/awk, or `sed -n`, and it is not `cat > file`.
9. **`shell_other`:** everything else (git diff/log, pip, mkdir, compilers, linters…).

### `error`
| case | rule |
|---|---|
| Content kinds (`file_view`, `search`, `edit_ack`, `tool_ack`) | Only tool-level failures count: "No such file", "does not exist", "command not found", "Permission denied", "No replacement was performed", "did not appear verbatim", "introduced new syntax error", "NOT been applied", "ERROR:", "Error:" at line start, etc. Source code containing `ValueError` does not count. |
| Execution kinds | Strong markers: Traceback, command not found, No such file, `FAILED`, `fatal:`, Permission denied, `XxxError: ` at line start, pytest `E   …Error`, `error: `/`error[E…]: `, Syntax/Import/ModuleNotFound errors. |
| Any kind | A non-zero `exit_code` counts as an error (leaderboard `status == error`, or the OpenHands footer exit code). The exception is exit code 1 on `search`, which is grep's "no match". |

- `error_regex_raw` is the pilot's looser regex family (Traceback / `\w+Error` / `error` / command not found / No such file / FAILED / fatal / Permission denied) applied to the raw text. It is kept for comparison; it fires on about 18–29% of observations, mostly because of source code inside file views.
- `exit_code` is null on SWE-smith, which doesn't record it.

### `tests_pass` (`test_run` only)
- Parsed from the last pytest summary line (`=== … in Xs ===`, or the `-q` form) with ANSI codes stripped.
  - `False` if the line contains failed or error(s);
  - `True` if it contains passed;
  - otherwise `null` (e.g. "no tests ran").
- Unittest: `Ran N tests` followed by `OK` or `FAILED (`.
- `null` also covers output piped through `head`/`tail`, where the summary is not shown.

### `truncated`
Set when the content contains a scaffold or dataset truncation marker (`<response clipped>`, "Observation truncated", `<... tool result truncated ...>`, "output truncated", SWE-agent's "Observations should not exceeded"), or when the leaderboard event has `truncated: true`. Nebius caps results at 64 KB, keeping the first and last 32 KB.

The generic phrase "too long" was dropped as a marker because it matched linter messages such as "E501 line too long".

## Statistics
| | SWE-smith | Leaderboard 2026 | OpenHands (old) |
|---|---|---|---|
| trajectories / tasks / repos | 300 / 300 / 115 | 150 / 86 / 66 | 150 / 150 / 126 |
| Qwen3 tokens p10 / p50 / p90 / max | 4,518 / 12,066 / 28,191 / 83,864 | 14,921 / 32,711 / 76,600 / 177,818 | 32,817 / 48,181 / 69,166 / 117,201 |
| share > 32k tokens | 7% | 49% | 91% |
| byte share obs / action / thought / task / markup | 55% / 15% / 20% / 8% / 2% | 74% / 12% / 4% / 8% / 2% | 67% / 17% / 5% / 7% / 4% |
| observations (empty) | 4,273 (0) | 5,942 (162) | 9,186 (289) |
| `file_view` n, byte share, error rate | 1009, 49%, 2% | 1740, 45%, 3% | 1996, 24%, 5% |
| `test_run` n, byte share, error rate | 76, 1%, 8% | 785, 17%, 22% | 1174, 52%, 21% |
| `python_exec` n, byte share, error rate | 1118, 10%, 29% | 1313, 11%, 18% | 1752, 8%, 23% |
| `search` n, byte share, error rate | 458, 9%, 0% | 1288, 12%, 2% | 1701, 8%, 1% |
| `edit_ack` n, byte share, error rate | 1211, 13%, 3% | 350, 9%, 9% | 1542, 5%, 3% |
| `shell_other` n, byte share, error rate | 214, 1%, 2% | 466, 7%, 11% | 502, 3%, 3% |
| `tool_ack` n, byte share, error rate | 187, 17%, 6% | – | 519, 0%, 0% |
| error rate strict / raw regex | 9.5% / 28.5% | 9.6% / 29.1% | 9.0% / 17.6% |
| test runs pass / fail / null | 69 / 5 / 2 | 428 / 130 / 227 | 735 / 133 / 306 |
| truncated observations | 51 (1.2%) | 10 (0.2%) | 249 (2.7%) |

## Caveats
- **Long trajectories versus a 32k window:** SWE-smith 7% over 32k tokens (p50 12,066); Leaderboard 2026 49% over 32k tokens (p50 32,711); OpenHands (old) 91% over 32k tokens (p50 48,181). Scorers that keep a prefix lose the late turns, which is where most test runs happen.
- **SWE-smith:**
  - The tasks are synthetic bugs injected into public repos, and the repos themselves are in pretraining data.
  - It has few `test_run` observations (76), because Claude 3.7 mostly ran its own reproduction scripts (`python_exec`).
  - The dataset predates Nemotron-Terminal; whether Nemotron's SFT corpus includes SWE-smith is not verified.
- **Leaderboard 2026:**
  - It has only 110 tasks, so 150 trajectories reuse 64 tasks across two teachers.
  - Picking the shortest resolved run biases it toward efficient runs.
  - GPT-5.4 and Gemini give no visible reasoning, so their thought spans are empty.
  - Scaffold-error turns (unparseable tool calls) are stubs, not real text.
- **OpenHands:** in addition to the self-family bias and pre-cutoff dates above, observations include OpenHands' own `cat -n` and editor framing, and about 2.7% of results are truncated by the scaffold.
- **Labels** are heuristic. A 15-observation spot check gave obs_kind 15/15 and error 14/15 before the last regex fix (an edit "introduced new syntax error" result had been labelled as no error; now fixed). Compound commands are labelled by their first non-echo program.
