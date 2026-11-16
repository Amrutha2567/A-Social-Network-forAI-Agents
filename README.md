Problem 1: A Social Network forAI Agents
Build a platform where AI agents from different companies (e.g. Swiggy, Flipkart, PhonePe,
HDFC Bank, Bajaj Auto) post and talk to each other, much like Twitter for agents.
Core flow
1. Post: An agent finds information (an offer, an announcement, a market update) and
publishes it to the platform as a post.
2. Route: The platform works out which other agents would find the post relevant and
notifies only them.
3. Respond: Each notified agent decides whether to engage. If it does, it uses an LLM to
draft a response and adds it as a comment on the post.
Example
Swiggy's agent posts: "5% off all deliveries on Diwali."
The platform notifies PhonePe and HDFC Bank, since payments and cards tie in to this
offer. It doesn't notify Bajaj Auto. PhonePe's agent replies with a comment: "Extra ₹50
cashback when you pay for Swiggy orders with PhonePe UPI on Diwali."
What we want you to design or build
How agents register and describe what they care about
How the platform decides who is relevant to a post (the core problem)
How notifications reach agents, and how agents post and comment back
APIs and data model for agents, posts, comments and subscriptions
Things to think about
Relevance quality: how you avoid both spam and missed matches
Scale: thousands of agents and a high volume of posts
Trust and safety: verifying agents, stopping false or abusive posts
Feedback: whether the platform learns from which notifications led to comments
Interview Problems: AI Engineering

Page 1 of 3

Interviewer note: Treat "sourcing from the internet" as a black box so the time goes
into relevance routing, which is the most interesting part.

Problem 2: A Hardware Q&A Assistant for Your Linux Laptop
Build a chatbot that runs locally on a Linux laptop and answers questions about that
machine's hardware in plain language.
Core flow
1. Ask: The user types a natural-language question, e.g. "How much RAM do I have?" or
"Is my SSD NVMe?"
2. Gather: The assistant works out what information it needs and collects it from the
system (e.g. lscpu , lsblk , free , lspci , dmidecode , /proc , /sys ).
3. Answer: It turns the raw output into a clear, accurate answer.
Example
User: "Can I add more RAM, and how much?"
The assistant checks the installed memory, the slots in use and free, and the maximum
capacity the board supports. It replies: "You have 16 GB in 1 of 2 slots. The board supports
up to 64 GB, so you can add a stick of up to 32 GB."
What we want you to build
A chat interface (CLI is fine)
A way for the LLM to call system-inspection tools, rather than guessing
Parsing and normalising command output into structured data
Handling follow-ups ("and what about the GPU?")
Things to think about
Safety: commands should be read-only and allow-listed, with no arbitrary shell
execution
Permissions: some data needs root (e.g. dmidecode ), so how do you handle that?
Accuracy: how the assistant avoids hallucinating specs and says "I don't know" when
it should
Portability: differences across distros and hardware, and tools that may be missing
Privacy: whether data leaves the machine, and whether a local model is an option
