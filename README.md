# Rampage

A modular Discord bot framework built with discord.py.

## What's this?

Rampage is a Discord bot that uses a module system to organize features. Each module can have its own commands, events, and logic. You can enable different modules per server, which is pretty handy if you're running the bot across multiple Discord guilds.

## Setup

Install dependencies:
```bash
pip install -r requirements.txt
```

Create a `.env` file with your bot token:
```
DISCORD_TOKEN=your_token_here
```

Run it:
```bash
python rampage.py
```

## How modules work

Modules live in the `modules/` directory. Each one is self-contained with its own folder structure. The module manager handles loading and enabling them automatically.

To enable a module globally, add it to `ENABLED_MODULES` in `rampage.py`. For guild-specific modules, use the `GUILD_ENABLED_MODULES` dict with the guild ID as the key.

## Project structure

```
rampage.py          # Main entry point
architecture/       # Core module management system
modules/            # Your bot modules go here
  example/          # Example module
  rampage/          # Core rampage module
```

That's about it. Check out the example module to see how to build your own.
