# Getting started

This bot is a sketch. It can research, compare, and run small local tests. It cannot spend money, create accounts, or contact anyone for you.

1. **Set up its workspace (first run only, about a minute).** A template carries only text, so the bot fetches its own small tool kit from the public repo (`github.com/Markcial/bots`, folder `superconnected-research-entity/kit`) onto its computer.

   First message to try: `Set up your workspace.`

   It tells you what it will do and asks for your yes first. The kit needs only `curl` and `git`, and everything is free with no account. It runs a self-check and shows you the result: a test experiment folder, a test report, and the link checker run against one good and one broken URL. It saves the folder in the memory note `workspace-path`. If a step would need a paid account, it stops and asks.
2. **Give it a real question** and the decision it feeds. Say your budget. If you say nothing, the budget is zero and it looks for free options first.

   First message to try: `Compare the free ways to <do something>. Cite every claim and flag any cost.`

3. **Read the report.** The conclusion comes first, then the evidence, your opinion kept apart, the options with price, free-tier limits, and what happens after them, the costs, and a list of what it could not verify.
4. **Open two of the links.** Every factual sentence has a title and a URL. The bot runs a link check before it hands over a report, and pastes the result at the bottom. If a claim has no source, it has to fix it or delete it.
5. **Ask for a small experiment** when an opinion is not enough. It makes a folder with the question, the hypothesis, what would prove it wrong, the exact commands, the raw results, and a conclusion. It runs the test with free tools and shows you the results.
6. **Expect a stop** when a step needs money, an account, or contact with a person. It asks for a yes to that exact action. Silence is not approval, and a yes for one step does not cover another.
7. **Optional routines.** Tell it which topics to watch and which tools to compare. It saves them as the memory notes `watch-list` and `tool-shortlist`. The Monday watch and the monthly price check read those notes.
8. **Without web access** it says what it could not check and asks you for sources. It does not invent them.
