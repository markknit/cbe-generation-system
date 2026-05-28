# Handoff Prompt — User's Instructions for the New Account Session

> This is the verbatim handoff prompt the user wrote to brief the first
> Claude/Claude Code session under the new non-profit business account.
> Captured here so the new session has direct access to the user's intent
> in their own words.

---

I'm going to continue an existing project that was initiated via the Claude.ai
interface, but as a formal project using Claude Code. The project is focused on
developing lesson plans for Kenyan teachers that are moving to the new CBE
curriculum model. The project is large and will be run across (at least) 3
systems to optimize timeframe to execute and minimize overall cost: the
Claude.code interface as needed, the Anthropic API, and an Nvidia Spark
processor with a Blackwell GPU and 128GB of Ram. The Spark will be accessed via
an Nvidia Sync connection and Tailscale SSH connections as needed.

As the project is moved and restarted there are a few important input documents
inside the cbe-generation-system folder:

- A Claude.md document to state the overall interface parameters of the entire
  account
- A project.md file called CBE_Project_Context_040326.md that documents the
  current status before adding new instructions.
- A new set of additional instructions that will outline changes to the content
  and structure of the lesson plans in the folder
  `\users\mrkni\cbe-generation-system`. This is titled `Overview to Claude.docx`.
  It is important to note that these instructions are NOT intended to replace or
  eliminate the previous instructions – merely to enhance the detail and clarity
  and add some new sections to the lesson plans. The formatting should stay the
  same as what we are using now.
- The previous templates that were used as reference.
- The relevant Kenyan curriculums.
- New templates that will contain the new sections that need to be added to the
  standard lesson plan output.

**Notes:**

- Please make sure to read the new set of additional instructions are stored in
  a file folder titled `Project_update_040726` inside the
  `\users\mrkni\cbe-generation-system` folder on this Windows notebook, which
  is now synced with github. Please start with the `Overview to Claude.docx`
  file for instructions.
- Please make sure that the lesson plan format from the most recent test
  generation is maintained.
- If there are any inconsistencies that you discover between the previous and
  the new instructions, or any missing instructions or data required – please
  do not hesitate to ask me for guidance.
- You should already have access to the Anthropic API information. If not,
  please advise me.
