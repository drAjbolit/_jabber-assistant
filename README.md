# _jabber-assistant

Personal AI assistant for Jabber/XMPP.

## Features

- Connect to existing Chrome session via CDP
- Listen for incoming Jabber messages via Strophe.js hooks
- Send messages through Jabber Web
- Bridge conversations with ChatGPT

## Status

🚧 Early prototype

## Current status

- Chrome CDP connection works
- Jabber tab detection works
- ChatGPT tab detection works
- Incoming XMPP messages intercepted via Strophe.js
- Outgoing messages sent through textarea automation

## Architecture

XMPP -> Strophe Hook -> Python -> ChatGPT -> Jabber