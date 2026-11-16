# Problem 2 – Linux Hardware Q&A Assistant

This must run on Linux. On Windows, use WSL2 Ubuntu.

## Install system utilities (Ubuntu/WSL)
```bash
sudo apt update
sudo apt install -y python3-venv pciutils dmidecode util-linux procps
```
## Install Python package
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```
## Optional offline LLM
Install Ollama using its official Linux instructions, then:
```bash
ollama pull qwen2.5:3b
ollama serve
```
Set `USE_OLLAMA=false` in `.env` to use deterministic JSON output only.

## Run
```bash
python -m hw_assistant.cli status
python -m hw_assistant.cli inspect
python -m hw_assistant.cli ask "How much RAM is installed?"
python -m hw_assistant.cli ask "Can I upgrade my RAM and how many slots are free?"
python -m hw_assistant.cli ask "What GPU is installed?"
```

## Security and limitations
The LLM never creates shell commands. Only fixed commands from `ALLOW_LIST` can execute; arguments are fixed, `shell=False` is used, and commands time out after five seconds. User text is never inserted into a shell command. The LLM receives normalized JSON and is instructed not to guess.

Some DMI fields require elevated privileges. This MVP does not run the whole assistant as root and does not call sudo automatically; if access is denied it reports the error. For production, use a narrowly scoped privileged helper/Unix socket or carefully audited sudoers rule for only the read-only command. Add distro-specific parser tests, capability discovery, session caching, structured logs and a stronger constrained intent classifier. Keep hardware data local.
