# Starsky Bot

Starsky Bot is a Discord bot that interacts with the Starsky API to generate documents and images using AI. This bot allows you to create documents based on templates, retrieve account information, and generate images based on prompts.

## Features

- Create documents using various templates.
- Generate images using the Starsky AI.
- Retrieve account information from Starsky API.
- Set up your Starsky API key for authentication.

## Commands

### `$account`

Retrieve information about your Starsky account, including account name, plan name, total words, and used words.

### `$templates [template_id]`

View available templates or create a new document using a selected template. If a `template_id` is provided, the bot will guide you through creating a document with the chosen template.

### `$image [prompt]`

Generate an image using the Starsky AI based on the provided prompt. This command allows you to interactively regenerate images by reacting with 🔄.

### `$setup`

Set up your Starsky API key to authenticate with the bot. Follow the prompts to provide your API key.

### `$help`

Display a help message with information about available commands.

## Getting Started

1. Invite the bot to your Discord server.
2. Run the `$setup` command and provide your Starsky API key to authenticate.
3. Explore available commands to generate documents and images.

## Dependencies

- discord.py
- requests

## Note

- Ensure that you've obtained your Starsky API key from https://starsky.pro/developers before using the bot.

## Customization

Feel free to modify and customize this code to better suit your requirements. Whether you want to add new features, adjust command behavior, or integrate additional APIs, this code serves as a starting point for your own creative ideas. You're encouraged to make changes, experiment, and adapt the bot to your specific use cases.

## License

This project is licensed under the [MIT License](LICENSE).

