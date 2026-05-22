from __future__ import annotations

import json
import re
from pathlib import Path

from story_automator.core.agent_config import AgentConfigResolved, build_agents_file, load_agent_config_from_state, parse_agent_config_json, resolve_agent_for_task, resolve_agents_payload
from story_automator.core.agent_plan import agent_plan_error, load_agents_plan_for_resolution, load_complexity_payload
from story_automator.core.diagnostics import issues_from_exception
from story_automator.core.frontmatter import find_frontmatter_value, parse_frontmatter
from story_automator.core.sprint import sprint_status_epic
from story_automator.core.story_keys import normalize_story_key
from story_automator.core.utils import file_exists, get_project_root, print_json, read_text, trim_lines


def check_epic_complete_action(args: list[str]) -> int:
    if len(args) < 2:
        print_json({"ok": False, "error": "epic_number and story_id required"})
        return 1
    epic, story = args[0], args[1]
    state_file = ""
    tail = args[2:]
    for idx, arg in enumerate(tail):
        if arg == "--state-file" and idx + 1 < len(tail):
            state_file = tail[idx + 1]
    if story.split(".", 1)[0] != epic:
        print_json({"ok": True, "isLastStory": False, "epic": int(epic), "storyId": story, "reason": "story_not_in_epic"})
        return 0
    stories: list[str] = []
    if state_file and file_exists(state_file):
        story_range = parse_frontmatter(read_text(state_file)).get("storyRange", [])
        stories = [sid for sid in story_range if isinstance(sid, str) and sid.startswith(f"{epic}.")]
        source = "state_file"
    else:
        stories, _ = sprint_status_epic(get_project_root(), epic)
        source = "sprint_status"
    if stories:
        stories = sorted(set(stories), key=lambda item: tuple(int(part) for part in item.replace("-", ".").split(".")[:2]))
        last = stories[-1]
        print_json({"ok": True, "isLastStory": story in {last, last.replace("-", ".")}, "epic": int(epic), "storyId": story, "lastInEpic": last, "epicStoryCount": len(stories), "source": source})
        return 0
    print_json({"ok": True, "isLastStory": False, "epic": int(epic), "storyId": story, "reason": "could_not_determine", "source": "fallback"})
    return 0


def get_epic_stories_action(args: list[str]) -> int:
    if not args:
        print_json({"ok": False, "error": "epic_number_required"})
        return 1
    epic = args[0]
    state_file = ""
    tail = args[1:]
    for idx, arg in enumerate(tail):
        if arg == "--state-file" and idx + 1 < len(tail):
            state_file = tail[idx + 1]
    if state_file and file_exists(state_file):
        stories = [sid for sid in parse_frontmatter(read_text(state_file)).get("storyRange", []) if isinstance(sid, str) and sid.startswith(f"{epic}.")]
        if stories:
            print_json({"ok": True, "epic": epic, "stories": stories, "count": len(stories), "source": "state_file"})
            return 0
    stories, _ = sprint_status_epic(get_project_root(), epic)
    if stories:
        print_json({"ok": True, "epic": epic, "stories": stories, "count": len(stories), "source": "sprint_status"})
        return 0
    epic_file = find_epic_file(epic)
    if epic_file:
        stories = sorted(set(re.findall(rf"\b{re.escape(epic)}\.\d+", read_text(epic_file))), key=lambda item: tuple(int(part) for part in item.split(".")))
        if stories:
            print_json({"ok": True, "epic": epic, "stories": stories, "count": len(stories), "source": "epic_file"})
            return 0
    print_json({"ok": False, "epic": epic, "error": "no_stories_found", "count": 0})
    return 0


def check_blocking_action(args: list[str]) -> int:
    if not args:
        print_json({"ok": False, "error": "story_id_required"})
        return 1
    norm = normalize_story_key(get_project_root(), args[0])
    if norm is None:
        print_json({"ok": False, "error": "could_not_normalize_key", "input": args[0]})
        return 1
    epic = norm.id.split(".", 1)[0]
    epic_file = find_epic_file(epic)
    if not epic_file:
        print_json({"ok": True, "blocking": True, "story": norm.id, "epic": epic, "dependents": [], "reason": "epic_file_not_found", "source": "unknown"})
        return 0
    dependents: list[str] = []
    current_story = ""
    for line in trim_lines(read_text(epic_file)):
        match = re.match(r"^###\s+Story\s+(\d+\.\d+):", line)
        if match:
            current_story = match.group(1)
            continue
        if current_story and re.search(r"(?i)Dependencies:|\*\*Dependencies\*\*:", line):
            if norm.id in line or norm.prefix in line:
                dependents.append(current_story)
    if dependents:
        print_json({"ok": True, "blocking": True, "story": norm.id, "epic": epic, "dependents": sorted(set(dependents)), "reason": "dependent_stories", "source": "epic_file"})
        return 0
    print_json({"ok": True, "blocking": False, "story": norm.id, "epic": epic, "dependents": [], "reason": "no_dependents_found", "source": "epic_file"})
    return 0


def agents_build_action(args: list[str]) -> int:
    options = {"state-file": "", "complexity-file": "", "output": "", "config-json": ""}
    idx = 0
    while idx < len(args):
        key = args[idx].lstrip("-")
        if idx + 1 < len(args):
            options[key] = args[idx + 1]
            idx += 2
        else:
            idx += 1
    if not all(options.values()) or not file_exists(options["state-file"]) or not file_exists(options["complexity-file"]):
        print_json({"ok": False, "error": "missing_args" if not all(options.values()) else "file_not_found"})
        return 1
    _, issues = load_complexity_payload(options["complexity-file"])
    if issues:
        print_json(agent_plan_error("invalid_complexity_json", issues))
        return 1
    try:
        payload = build_agents_file(options["state-file"], options["complexity-file"], options["output"], options["config-json"])
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print_json(agent_plan_error("invalid_agent_config", issues_from_exception(exc, source="agent-plan", field="config-json")))
        return 1
    print_json(payload)
    return 0


def agents_resolve_action(args: list[str]) -> int:
    options = {"state-file": "", "agents-file": "", "story": "", "task": ""}
    idx = 0
    while idx < len(args):
        key = args[idx].lstrip("-")
        if idx + 1 < len(args):
            options[key] = args[idx + 1]
            idx += 2
        else:
            idx += 1
    if not options["story"] or not options["task"] or (not options["state-file"] and not options["agents-file"]):
        print_json({"ok": False, "error": "missing_args"})
        return 1
    agents_path = options["agents-file"] or find_frontmatter_value(options["state-file"], "agentsFile")
    if not agents_path or not file_exists(agents_path):
        print_json({"ok": False, "error": "agents_file_not_found"})
        return 1
    agents_plan, issues = load_agents_plan_for_resolution(agents_path, options["story"], options["task"])
    if issues:
        print_json(agent_plan_error("invalid_agents_json", issues))
        return 1
    payload = resolve_agents_payload(agents_plan, options["story"], options["task"])
    print_json(payload)
    return 0 if bool(payload.get("ok")) else 1


def retro_agent_action(args: list[str]) -> int:
    options = {"state-file": ""}
    idx = 0
    while idx < len(args):
        key = args[idx].lstrip("-")
        if idx + 1 < len(args):
            options[key] = args[idx + 1]
            idx += 2
        else:
            idx += 1
    if not options["state-file"]:
        print_json({"ok": False, "error": "missing_args"})
        return 1
    if not file_exists(options["state-file"]):
        print_json({"ok": False, "error": "file_not_found"})
        return 1
    try:
        config = _load_agent_config_from_state(options["state-file"])
    except (json.JSONDecodeError, OSError, ValueError) as exc:
        print_json(agent_plan_error("invalid_agent_config", issues_from_exception(exc, source="agent-plan", field="state-file")))
        return 1
    primary, fallback = resolve_agent_for_task(config, "medium", "retro")
    print_json({"ok": True, "task": "retro", "primary": primary, "fallback": fallback})
    return 0


def find_epic_file(epic: str) -> str:
    root = Path(get_project_root())
    for pattern in (f"_bmad-output/implementation-artifacts/epic-{epic}-*.md", f"docs/epics/epic-{epic}-*.md"):
        matches = sorted(root.glob(pattern))
        if matches:
            return str(matches[0])
    return ""


def parse_agent_config(raw: str) -> dict:
    config = parse_agent_config_json(raw)
    return {
        "defaultPrimary": config.default_primary,
        "defaultFallback": config.default_fallback,
        "perTask": {
            task: {"primary": task_config.primary, "fallback": task_config.fallback}
            for task, task_config in config.per_task.items()
        },
        "complexityOverrides": {
            level: {
                task: {"primary": task_config.primary, "fallback": task_config.fallback}
                for task, task_config in task_map.items()
            }
            for level, task_map in config.complexity_overrides.items()
        },
    }


def resolve_agent(config: dict, level: str, task: str) -> tuple[str, str]:
    return resolve_agent_for_task(_legacy_config_to_core(config), level, task)


def _load_agent_config_from_state(state_file: str) -> AgentConfigResolved:
    return load_agent_config_from_state(state_file)


def _legacy_config_to_core(config: dict) -> AgentConfigResolved:
    return parse_agent_config_json(
        json.dumps(
            {
                "defaultPrimary": config.get("defaultPrimary", "auto"),
                "defaultFallback": config.get("defaultFallback", "false"),
                "perTask": config.get("perTask", {}),
                "complexityOverrides": config.get("complexityOverrides", {}),
            }
        )
    )
