<p align="center">
  <img src="https://starsky.pro/uploads/brand/cEKpGkKA8tD5P2nKh47CsigASMEwJCWRn4k3dRW5.png" alt="Starsky Bot Logo" width="200">
</p>

# Starsky Bot

Starsky Bot is a Discord bot that interacts with the Starsky API to create documents and generate images using AI. This bot offers features such as document generation with templates, image generation, account information retrieval, and API key setup.

## Features

- Generate documents with various templates.
- Create AI-generated images using Starsky AI.
- Retrieve and display account information from Starsky API.
- Set up your Starsky API key for authentication.

## Commands

### `$account`

Retrieve detailed account information including account name, plan, total words, and usage statistics.

### `$templates [template_id]`

View available templates or generate a new document using a specific template. Provide `template_id` to create a document.

### `$image [prompt]`

Generate an image using the Starsky AI, based on the provided prompt. Regenerate images interactively with 🔄 reactions.

### `$setup`

Configure your Starsky API key for bot authentication. Follow the prompts to input your API key.

### `$help`

Display a comprehensive help message with an overview of available commands.

## Getting Started

1. Invite the bot to your Discord server.
2. Create a `config.json` file in the root directory and configure it as follows:

   ```json
   {
       "bot_token": "YOUR_DISCORD_BOT_TOKEN",
       "api_key": "YOUR_STARSKY_API_KEY"
   }

## Dependencies

- discord.py
- requests

## Note

- Ensure that you've obtained your Starsky API key from https://starsky.pro/developers before using the bot.

## Installation

Before starting the bot, run the `install.sh` script to install the required dependencies:

```bash
chmod +x install.sh
./install.sh

## Customization

Feel free to modify and customize this code to better suit your requirements. Whether you want to add new features, adjust command behavior, or integrate additional APIs, this code serves as a starting point for your own creative ideas. You're encouraged to make changes, experiment, and adapt the bot to your specific use cases.

## License

This project is licensed under the [MIT License](LICENSE).

---

To run the bot, make sure to insert your Discord bot token at the end of the `bot.py` file:

```python
bot.run('YOUR TOKEN GOES HERE')
