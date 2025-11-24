# AI Learning Repository - Agent Instructions

## Project Overview

This repository is designed for learning and experimenting with AI tools. It serves as a structured workspace where different AI-assisted projects can coexist while maintaining clear organization and documentation.

## Repository Structure

This repository contains multiple subproject folders, each representing a completely independent project for learning different aspects of AI-assisted development. Each subproject must maintain its own prompt history for learning and reference purposes.

### Current Subprojects
1. `TODO_LIST/` - Task management application
2. `[Future Project 2]/`
3. `[Future Project 3]/`
4. `[Future Project 4]/`
5. `[Future Project 5]/`

## Critical Rules - ALWAYS FOLLOW

### 1. Prompt Logging (MANDATORY)

**Every single user prompt MUST be logged to the appropriate subproject's `prompts-list.txt` file.**

When a user interacts with a specific subproject:
1. Identify which subproject folder the work relates to
2. Open or create the `prompts-list.txt` file in that subproject folder
3. Append the user's prompt to the file
4. Separate each prompt with a line of dashes (73 dashes exactly)

**Format for prompts-list.txt:**
```
User prompt text goes here...
This can be multiple lines.
-------------------------------------------------------------------------
Next user prompt goes here...
-------------------------------------------------------------------------
```

**Important:**
- Log prompts BEFORE starting work on the request
- Include the full, original user prompt without modification
- Do not skip this step - it's for learning and documentation purposes
- Each subproject maintains its own separate prompts-list.txt

### 2. Subproject Organization

Each subproject folder MUST contain:
- `prompts-list.txt` - Log of all user prompts for this subproject
- Project-specific code, files, and folders
- Any project-specific documentation

### 3. Subproject Independence

- Each subproject is completely independent
- Do not mix code or concerns between subprojects
- Each subproject can have its own tech stack, patterns, and structure
- Treat each subproject as if it were its own repository

### 4. When Working on a Subproject

Before implementing any changes:
1. **First:** Log the user prompt to `[subproject]/prompts-list.txt`
2. **Then:** Proceed with the requested work
3. Keep all work within the appropriate subproject folder

### 5. Environment and Configuration

- `.env` file is in the root for API keys (NEVER commit this)
- `opencode.json` is the root configuration (project-wide)
- `plan.md` is the root prompt for the plan agent
- Root-level files affect all subprojects

## Agents Available

### Plan Agent
- Software architect for analysis and planning
- Read-only mode - creates plans but doesn't edit code
- Use for: Understanding requirements, designing solutions, analyzing architecture
- Switch to this agent (Tab key) when you need a plan before implementation

### Build Agent
- Implementation specialist
- Always works with test-provider subagent in parallel
- Use for: Implementing features, writing code, making changes
- Automatically ensures tests are created for all code

### Test-Provider Subagent
- Testing specialist
- Automatically invoked by build agent
- Creates comprehensive test coverage
- Can be manually invoked with @test-provider

## MCP Tools Available

### Context7
- Use for searching documentation and examples
- Invoke with "use context7" in prompts
- Requires CONTEXT7_API_KEY in .env for higher rate limits

## Best Practices

1. **Always log prompts first** - This is non-negotiable
2. **Use plan agent first** - For complex features, switch to plan agent to design before building
3. **Stay organized** - Keep each subproject self-contained
4. **Document as you go** - Each subproject should be understandable on its own
5. **Test everything** - Build agent always creates tests via test-provider

## Example Workflow

1. User: "I want to add a feature to the TODO_LIST project"
2. Agent: Logs prompt to `TODO_LIST/prompts-list.txt`
3. Agent: If complex, suggests switching to plan agent for design
4. Agent: Implements the feature in TODO_LIST folder
5. Agent: Ensures tests are created via test-provider
6. Agent: All work stays within TODO_LIST folder

---

**Remember:** This is a learning repository. The prompt logs are valuable for reviewing how problems were approached and solved. Never skip logging user prompts!
