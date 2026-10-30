# Offline Character Chat

AI character chat that runs entirely on your own computer: **browser + Ollama**, no account and no cloud. Your conversations stay on your PC, saved in the browser, and once Ollama and a model are downloaded no internet is needed.

You can create or import characters (roleplay or assistant), keep separate chats, and have the character remember the story through an automatic summary, pinned facts and a lorebook. There is a Character Creator, support for model thinking and an interface in Italian and English. Use it from the PC and, on the same Wi-Fi, from your phone.

## Contents

1. [Included files](#1-included-files)
2. [What you need](#2-what-you-need)
3. [Quick start (Windows)](#3-quick-start-windows)
4. [Manual start (Windows, Mac, Linux)](#4-manual-start-windows-mac-linux)
5. [Using it from your phone (same Wi-Fi network)](#5-using-it-from-your-phone-same-wi-fi-network)
6. [Shutting everything down](#6-shutting-everything-down)
7. [How to use the app](#7-how-to-use-the-app)
8. [Memory and automatic summary](#8-memory-and-automatic-summary)
9. [Lorebook](#9-lorebook)
10. [Settings](#10-settings)
11. [Import, export and backup](#11-import-export-and-backup)
12. [Where your data lives](#12-where-your-data-lives)
13. [Troubleshooting](#13-troubleshooting)
14. [Known limits](#14-known-limits)
15. [Working without internet](#15-working-without-internet)
16. [Creating the `.bat` files from scratch](#16-creating-the-bat-files-from-scratch)

## 1. Included files

Keep them all in the same folder, with these names.

| File | What it is |
|---|---|
| `offline-character-chat.html` | the whole app (HTML, CSS, JavaScript) |
| `avvia-chat.bat` | double-click start, this PC only |
| `avvia-chat-rete.bat` | double-click start, PC + phone |
| `server.py` | server used by `avvia-chat-rete.bat` |
| `README_IT.md` | this guide in Italian |
| `README_EN.md` | this file (English) |

To use it on the PC only, the HTML and `avvia-chat.bat` are enough. The messages shown in the black `.bat` window are in Italian.

## 2. What you need

- **Ollama** ([ollama.com](https://ollama.com)), running, with at least one model downloaded:

  ```bash
  ollama pull qwen3:8b       # download a model
  ollama pull llama3.2:3b    # a lighter model
  ollama list                # list installed models
  ```

- **Python 3.7 or newer** ([python.org](https://www.python.org)). On Windows, tick *Add Python to PATH* during installation.
- A recent browser (Chrome, Edge, Firefox, Safari).
- The internet is only needed to download Ollama and the models. After that, everything works offline.

## 3. Quick start (Windows)

1. Start Ollama (separately: the app does not start it).
2. Double-click one of these:
   - `avvia-chat.bat`: this PC only
   - `avvia-chat-rete.bat`: this PC and also your phone ([section 5](#5-using-it-from-your-phone-same-wi-fi-network))
3. Your browser opens. Keep the black window open while you use the chat.

Use only one `.bat` at a time: both use port 8000 (the second one warns you if it is taken).

> Windows or your browser may flag `.bat` files as potentially dangerous: that is normal. You can open them with Notepad to see that they only contain a few commands. If you do not have them, or lost one, see [section 16](#16-creating-the-bat-files-from-scratch).

## 4. Manual start (Windows, Mac, Linux)

Start Ollama, then open a terminal in the folder with the files. On Windows, if `python` does not work, use `py`. On Mac/Linux use `python3`.

**This PC only:**

```bash
python server.py
```

then open <http://localhost:8000/>

**Also from your phone** (the terminal shows the address to open on the phone):

```bash
python server.py --lan
```

**Another port** (if 8000 is taken):

```bash
python server.py 9000
python server.py --lan 9000
```

**Simple alternative**, this PC only, without `server.py`:

```bash
python -m http.server 8000 --bind 127.0.0.1
```

then open <http://localhost:8000/offline-character-chat.html>

Always use the same address: your data is tied to it ([section 12](#12-where-your-data-lives)).

> Opening the HTML by double-clicking it, without a server, is not recommended: Ollama refuses the requests unless you set the environment variable `OLLAMA_ORIGINS=*` and restart it. Your data would also be separate from the data saved on `localhost`.

## 5. Using it from your phone (same Wi-Fi network)

1. Start Ollama on the PC.
2. Run `avvia-chat-rete.bat` (or `python server.py --lan`). If Windows asks for network access, allow **private** networks.
3. On your phone, open the *Dal telefono* ("from the phone") address shown in the window, something like `http://192.168.1.23:8000/`.
4. You do not need to set anything else: the Ollama URL fills itself in.

**How it works:** `server.py` serves the page and forwards **only** `/api/chat`, `/api/tags` and `/api/show` to Ollama (the last one tells the app whether the model supports thinking). Ollama itself is not opened to the network, so you do not need the `OLLAMA_HOST` or `OLLAMA_ORIGINS` variables. Every other path answers 404.

> **Warning:** anyone on your Wi-Fi can use the chat, and therefore your Ollama. Only use it on a trusted home network.

The phone's chats are separate from the PC's (data lives in each device's browser). To move them, use export and import ([section 11](#11-import-export-and-backup)). Importing a PC backup on the phone does not touch the phone's Ollama URL.

**If the shown address does not work:** phone and PC must be on the same Wi-Fi; if the PC has several network adapters (for example a VPN) try the IPv4 address you see with `ipconfig`; check that the firewall allowed the private network.

## 6. Shutting everything down

- **Chat:** close the black window (or press `Ctrl+C` inside it). Closing only the browser tab does not stop the server.
- **Ollama:** icon near the clock, right-click, *Quit Ollama*. While it is running it uses memory, especially with a model loaded.

Chats and memory stay saved in the browser.

## 7. How to use the app

### Left sidebar

On a phone it opens with the button at the top.

- **Chat tab:** all chats, most recent first. At the top choose the character and press **+ Chat** to start a new one. On each chat: ✎ = rename, ⇩ = export, × = delete.
- **Characters tab:** search, **+ New character**. On each character: **+** = new chat, ✎ = edit. Clicking the name starts a new chat right away and switches to the Chat tab.
- **At the bottom:** import character, chat or backup; below it, the language menu and the **Reset** button.

### Separate chats

Every chat is independent: it has its own history, pinned facts, summary and memory/summary switches. You can have as many chats as you like with the same character without them affecting each other. What is global: lorebook, your persona and settings.

### Writing

- `Enter` sends the message, `Shift+Enter` starts a new line. On a phone, Enter starts a new line: use the **Send** button.
- Empty field + **Send**, or `/ai`: the character replies without you writing anything.
- `/sys text`: an instruction that only applies to the next reply (example: `/sys describe the room`).
- **Stop** interrupts the reply and keeps what was generated. Pressing Enter while the model is replying does **not** stop it: use the button.
- **Continue** resumes the last reply where it stopped (only active if the last message is from the character).

### On messages

- **Edit**, **Delete**.
- **Regenerate:** on the last message it creates a variant and the arrows move between variants. On an older message it deletes the ones after it (asks for confirmation). Not available for messages already summarized into memory.
- **Copy:** on code blocks.
- **Reasoning (thinking):** if it was on, above the reply there is a collapsible block with the model's reasoning.
- **Text:** code blocks, `` `code` ``, `**bold**`, `*actions*`. With a character in Assistant mode, also headings (`#`) and lists. Tables are not drawn.

### Character

Pencil, or **+ New character**.

| Mode | What it does |
|---|---|
| **Roleplay** | roleplay rules: stays in character, does not write for you, actions between `*asterisks*` |
| **Assistant** | no roleplay rules, low temperature (0.4), code in blocks |
| **Creator** | special mode: turns a description into a character card (see *Character Creator*) |

- **Description**, **Personality**, **Scenario**.
- **First message:** several greetings separated by a line with `---`; the first is shown, the others are variants.
- **Extra rules:** additional instructions for the model.
- **Reminder:** text repeated at the end of the prompt on every reply; it helps small models stay in character a lot.
- **Example dialogue:** only used as a style guide.
- In the texts you can use `{{char}}` (the character's name) and `{{user}}` (your name).
- Editing a character does not change the first message of chats that have already started.

### Default characters

Only two characters come built in:

- **Assistant:** help with coding and general questions.
- **Character Creator:** creates new characters.

You can edit or delete them: if you delete them they do not come back.

### Character Creator

Open it (Characters tab, or pick the Creator and press **+ Chat**) and describe in your message who you want, even in a few words, optionally with a scenario. Example:

> a cynical detective in a cyberpunk city

The active model (menu at the top) writes the full card: name, description, personality, scenario, first message, example dialogue and reminder. The character is added to the Characters list and the chat shows a summary with the buttons **New chat with …** and **Open card**.

- If the request is short, missing details (age, appearance such as hair color, personality, scenario…) are filled in by the model and written into the card, **without changing anything you asked for**.
- Every message creates a **new** character. To tweak one, use **Open card** (or ✎ in the list).
- The card is written in the language of your request.
- The Creator has no Regenerate and Continue: for another version, write the request again. **Stop** cancels the creation without adding anything.
- In the Creator's card, **Extra roleplay rules** accepts your own instructions on how to create (example: "always write three lines of example dialogue").
- If the model does not follow the format, you will see a warning and the text it wrote: try again, or use a larger model. Small models follow the format less reliably.

### Thinking (the model's reasoning)

Some models (for example qwen3 or deepseek-r1) can "reason" before answering. The app only allows it for characters in **Assistant** and **Creator** mode, including the built-in Assistant and Character Creator.

- Above the message field there is a **Thinking: off / Thinking: on** button. It only appears if the model selected at the top supports thinking (the app asks Ollama). If your version of Ollama cannot tell, the button stays visible: if the model does not actually support it, the reply still arrives, just without reasoning.
- It is **off by default** and the choice is remembered per character.
- For **Roleplay** characters thinking is always off and there is no option at all.
- When on, replies are slower and use more tokens. The app raises the reply limit by itself (at least 2048 tokens, 3000 for the Creator, within half of the context) so the reasoning does not use up the whole reply.
- The reasoning appears in a collapsible **Reasoning (thinking)** block above the reply: open while the model is reasoning, closed once the reply is finished.
- The reasoning is not sent back to the model in later messages, and memory summaries never use thinking.

### Your name in this chat

**Memory & options > Memory > Your name in this chat.** It only applies to that chat (it is not global): it is the name the model sees instead of "User" and the one shown on your messages; `{{user}}` in cards also becomes this name.

- Empty = your persona name is used (*Your persona*).
- Other chats do not change, not even those of the same character. The first message of a new chat uses your persona name.
- Up to 40 characters. It is also saved in the chat export.

### Your persona

**Memory & options > Your persona.** Name and description of who you are, valid for all chats. If you leave the default name ("You" in English, "Tu" in Italian), the model receives it as "User". In each chat you can use a different name (see *Your name in this chat*).

### Language

At the bottom of the left sidebar. Dropdown menu: **English** (default) and **Italiano**. The whole interface changes immediately and your choice is remembered. Anyone who was already using the app without ever choosing a language switches to English: to go back to Italian, choose Italiano in the menu.

- The built-in characters (Assistant and Character Creator in English, Assistente and Creatore Personaggi in Italian) change name and welcome text with the language, but only if you have not edited them: fields you changed stay as they are.
- Chats already written stay in the language they were written in.
- The interface language does not decide which language the model replies in: it replies in the language you write in.
- **Adding a language:** open `offline-character-chat.html` in a text editor, search for `LANGS` and add an entry next to `it` and `en`:
  - `n` = name shown in the menu
  - `loc` = date format (example `fr-FR`)
  - `you` = default name of the person writing
  - `m` = the translations (Italian text: text in the new language; the `en` entry shows how)

  Untranslated entries stay in Italian. The new language shows up in the menu by itself.

### Reset

Red button at the bottom of the left sidebar. It asks for confirmation, then erases **everything** (chats, characters, lorebook, your persona, settings) and starts over like the first launch: only the two built-in characters, English language, no chats. After a reset no chat is open: pick a character and press **+ Chat**.

> It cannot be undone: make a backup first ([section 11](#11-import-export-and-backup)).

### Model

Menu at the top: lists the models installed in Ollama. If you start Ollama after the page, the list updates by itself.

## 8. Memory and automatic summary

Ollama remembers nothing between requests: the app handles memory.

- The full chat is **always** saved. On every reply the model receives: rules and card, your persona, pinned facts, summary, relevant lore, the latest messages that fit in the context, and the reminder (pinned facts and summary only if they are on for that chat, see below).
- **Pinned facts** (**Memory & options > Memory**): you write them and the automatic summary never touches them. Put the facts that must never disappear there.
- **Automatic summary:** when the messages not yet summarized take up about three quarters of the available space, the oldest ones are summarized by the model into bullet points (about 25 at most), keeping the latest messages in full (up to 12). The text can be edited by hand.
- **Summarize old messages now** forces a summary; **Undo last summary** restores the previous one.
- **Per-chat switches** (**Memory & options > Memory**): every chat has two independent checkboxes, both on by default. Memory and summary are different things:
  - **Memory in this chat:** if you turn it off, the pinned facts are not sent to the model (the text stays saved and editable).
  - **Summary in this chat:** if you turn it off, the summary is neither created nor used, and **Summarize old messages now** is disabled. The model gets the latest messages that fit in the context, including those that were already summarized before, and you can regenerate from those messages too.
  - The latest messages of the chat are **always** sent to the model, whatever you choose. Lorebook entries are not triggered by words found in texts that are switched off.
  - They only apply to that chat: other chats, even of the same character, do not change. They are also saved in the chat export.
  - The **Automatically summarize old messages** option in Settings remains the global switch.
- A small model may leave out or get details wrong in the summary: check it now and then and move the important things into the pinned facts.
- Summaries never use thinking. In summaries, your messages carry the name you use in that chat.
- The panel shows how many messages have been summarized and how many tokens the last prompt used.
- Warnings at the bottom: if the card, memory and lore take up too much context, or if the prompt reaches the limit (in that case Ollama may discard part of the history): increase the context.

## 9. Lorebook

**Memory & options > Lorebook.** Each entry has keywords (separated by commas) and content.

- The entry goes into the prompt if a keyword appears in the latest messages, in the pinned facts or in the summary.
- A keyword matches from the start of a word: `dra` finds "dragon", but `ago` does not.
- Empty keywords = always-on entry.
- The lorebook is global (it applies to all chats). The inserted text is limited to about 15% of the context.
- **Export lore** saves the entries to a file.

## 10. Settings

**Memory & options > Settings.**

| Setting | What it does |
|---|---|
| **Ollama URL** | default `http://localhost:11434`. From a phone with `avvia-chat-rete` it sets itself |
| **Temperature** | creativity (higher = more varied) |
| **Top P**, **Top K** | word sampling |
| **Context (token)** | maximum prompt tokens (default 8192). More context = more RAM/VRAM and slower replies. If your PC struggles, try 4096 |
| **Max reply tokens** | maximum length of a reply (with thinking on it is raised automatically, see [section 7](#7-how-to-use-the-app)) |
| **Repeat penalty** | reduces repetition |
| **Automatically summarize old messages** | yes/no |
| **Trim replies cut off by the token limit…** | roleplay only: if a reply stops because of the limit, it is cut at the last complete sentence and you can carry on with **Continue** |
| **Export full backup** | see [section 11](#11-import-export-and-backup) |

## 11. Import, export and backup

### Exporting

| What | How |
|---|---|
| **Character** | ✎ on the character > **Export**. Only the card, without chats |
| **Chat** | ⇩ in the chat list. Contains messages, variants, pinned facts, summary, your name in that chat and the character's card |
| **Lorebook** | **Memory & options > Lorebook > Export lore** |
| **Everything** | **Memory & options > Settings > Export full backup**: characters, chats, lorebook, your persona and settings |

### Importing

A single button, at the bottom of the left sidebar. You can pick several files at once: the type is recognized automatically. Exported files carry a version number: the app also imports those from earlier versions (it upgrades them itself) and refuses those created by a newer version.

| File | What happens |
|---|---|
| **Character** | files from this app and SillyTavern-style JSON cards (if the card contains a lorebook, its entries are imported). PNG cards are not supported |
| **Chat** | it is linked to the character with the same name and description; if it does not exist it is created |
| **Lorebook** | the entries are added to the existing ones |
| **Full backup** | **replaces** all data (asks for confirmation). The device's Ollama URL is not changed |

Make a backup now and then: your data lives in the browser ([section 12](#12-where-your-data-lives)).

## 12. Where your data lives

- Chats, characters, lorebook and settings are saved in the browser (`localStorage`), **not** in the files' folder.
- They are tied to the address: `localhost:8000`, the phone's network address and a file opened by double-clicking all have separate storage. Always use the same address.
- The space is about 5 MB (depends on the browser): enough for many chats, but a *Browser storage is full* warning means you must make a backup and free up space.
- If the saved data turns out to be unreadable, the app starts from scratch and keeps a raw copy in the browser (key `occ_corrotto`).
- On startup the app fixes incomplete or hand-edited data by itself (invalid lists or texts, wrong numeric settings): valid data is never touched. A backup with the wrong structure is refused on import.
- **Do not keep two tabs** of the app open together in the same browser: each one saves all the data and the last one to save erases the other's changes. If you see the warning *Another tab changed the data*, reload the page before you continue.
- The data has a **version number**: when you update the app it converts itself. Before converting, the app keeps a copy of the old data in the browser (key `occ_pre_migrazione`), as long as it is under about 1.2 MB.
- If the data was created by a **newer** version of the app, the app leaves it untouched and shows a warning: update the app.
- Clearing the site's data in the browser erases everything.
- The **Reset** button ([section 7](#7-how-to-use-the-app)) erases everything and starts over: make a backup first.

## 13. Troubleshooting

- **"Cannot connect to Ollama"**: Ollama is off, or the URL in Settings is not the right one. The app retries by itself every few seconds.

- **"Model not found"**: Download it with `ollama pull model-name` and try again.

- **"Ollama: …" with a reason (for example not enough memory)**: This is Ollama's real error. Try a smaller model or lower the context.

- **"Empty reply"**: The model produced no text. With reasoning models try raising **Max reply tokens**.

- **The Thinking button does not appear**: The character must be in Assistant or Creator mode and the selected model must support thinking (example: qwen3). If you use the phone, update `server.py` too: it must forward `/api/show`.

- **With thinking on, the reply is empty or stops short**: The reasoning used up all the tokens: raise **Max reply tokens** in Settings, or turn thinking off.

- **Slow replies or the PC freezes**: Lower the context, use a smaller model (3B-8B), close other heavy programs.

- **"Python non trovato"** (in the `.bat`): Install Python from python.org ticking *Add Python to PATH*.

- **"La porta 8000 e' gia' in uso"** (port 8000 is already in use): Another server is running (maybe the other `.bat`): close its window, or use another port ([section 4](#4-manual-start-windows-mac-linux)).

- **It will not open from the phone**: See the end of [section 5](#5-using-it-from-your-phone-same-wi-fi-network).

- **I reopened the app and my chats are gone**: You are using a different address from the one used before ([section 12](#12-where-your-data-lives)).

- **Warning "data created by a newer version"**: You are using an app file older than your saved data. Use the latest `offline-character-chat.html`: in the meantime your data stays intact.

## 14. Known limits

Not available yet: avatars, conversation branching, several characters in the same chat, PNG cards, markdown tables, import of Perchance's native format. The `.bat` files are for Windows; on Mac and Linux use the manual start.

## 15. Working without internet

The app works **without internet**: a local network is enough (for example your home Wi-Fi even if the router is not connected to the internet), or just the PC on its own.

- **Nothing is loaded from the internet:** no fonts, scripts, images or external services. The only address in the code is Ollama on your own PC. This was tested by blocking every request to the internet and using chat, thinking, the Creator, language switching and import/export, also from another address on the local network the way a phone does: no request went out.
- **The internet is only needed once**, to download Ollama, the models and Python ([section 2](#2-what-you-need)).
- **Wi-Fi without internet:** PC and phone must be on the same network. `server.py` starts even when no name service (DNS) is reachable. If it finds no network at all, it says so in the black window.
- **If the router changes the PC's address:** use the address shown in the black window, which updates on every start (or reserve a fixed address for the PC in the router settings).
- **If the page does not open from the phone** and the phone says "connected, no internet": some phones, on a Wi-Fi without internet, prefer mobile data even for local pages. Turn mobile data off and try again.
- **With no network at all** (no Wi-Fi, no cable) you can only use the app from the PC with `avvia-chat.bat`; the phone cannot connect.

## 16. Creating the `.bat` files from scratch

If you lost a `.bat`, or the zip reached you without it, you can recreate it in two minutes with Notepad.

### What they are

A `.bat` (batch) file is a plain **text file** containing a list of Windows commands. When you double-click it, Windows runs them one after the other, as if you had typed them in a terminal. It is not a compiled program and installs nothing: inside there is only the text shown below, which you can read and check. It saves you from opening a terminal and typing the commands by hand ([section 4](#4-manual-start-windows-mac-linux)). `.bat` files only work on Windows; on Mac and Linux use the manual start.

### What they do

Neither one starts Ollama: turn it on separately.

**`avvia-chat.bat`** (this PC only):

1. Goes to the folder it is in and checks that `offline-character-chat.html` is there.
2. If a server is already running on port 8000, it only opens the browser and ends.
3. Looks for Python (`py` or `python`). If it cannot find it, it says so and tells you where to download it.
4. After a couple of seconds it opens the browser and starts a small web server (`python -m http.server`) reachable **only from this PC**.
5. The black window stays open while you use the chat: closing it shuts the server down. If the server stops because of an error, the window waits for a key so you can read it.

**`avvia-chat-rete.bat`** (PC and phone):

1. Checks that `server.py` and `offline-character-chat.html` are in the folder.
2. If port 8000 is already taken, it says so and stops, without starting a second server.
3. Looks for Python as above.
4. Opens the browser on the PC and starts `python server.py --lan`: it serves the page to every device on your Wi-Fi and forwards only `/api/chat`, `/api/tags` and `/api/show` to Ollama ([section 5](#5-using-it-from-your-phone-same-wi-fi-network)). The address to open on the phone appears in the window.

### How to create them (Windows)

1. Put `offline-character-chat.html` in a folder. For the network `.bat`, `server.py` must be in the same folder too. The `.bat` files must be **in the same folder** as these files.
2. Open **Notepad** (Start menu, type *Notepad*).
3. Copy all the code of `avvia-chat.bat` (block below) and paste it into the empty Notepad.
4. Choose **File, Save as** and go to the folder from step 1.
5. In the *Save as type* menu choose **All files (\*.\*)**. If you skip this, Windows adds `.txt` and the file will not run.
6. In *File name* type exactly `avvia-chat.bat`. If you see an *Encoding* menu, choose **ANSI**. Then press *Save*.
7. Repeat steps 2-6 for `avvia-chat-rete.bat`, if you want to use it from the phone.
8. Check the name in File Explorer. If it is called `avvia-chat.bat.txt`, file extensions are hidden: in *View, Show* turn on **File name extensions** and remove `.txt` from the name.
9. Double-click the `.bat`. The black window opens, then the browser.

Copy the code **without changing it**. The messages shown in the black window are in Italian, and letters with accents are written without them (`e'` instead of `è`) on purpose, so the file works with any encoding. Only the commands matter.

### Code of `avvia-chat.bat` (this PC only)

```bat
@echo off
setlocal
title Offline Character Chat
cd /d "%~dp0"

if not exist "offline-character-chat.html" (
  echo Non trovo offline-character-chat.html in questa cartella.
  echo Metti questo file .bat nella stessa cartella dell'HTML.
  pause
  exit /b 1
)

set "PORT=8000"
set "URL=http://localhost:%PORT%/offline-character-chat.html"

rem Se il server e' gia' acceso, apri solo il browser
netstat -ano | findstr /R /C:":%PORT% .*0.0.0.0:0" >nul 2>&1
if %errorlevel%==0 (
  echo Il server e' gia' attivo. Apro il browser.
  start "" "%URL%"
  exit /b 0
)

set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python non trovato. Installalo da https://www.python.org/downloads/
  echo e spunta "Add Python to PATH" durante l'installazione.
  pause
  exit /b 1
)

echo Offline Character Chat: %URL%
echo.
echo Tieni aperta questa finestra mentre usi la chat.
echo Chiudila per spegnere il server. Ollama va acceso a parte.
echo.

rem Apre il browser dopo 2 secondi, quando il server e' pronto
start "" /min cmd /c "ping -n 3 127.0.0.1 >nul & start %URL%"

%PY% -m http.server %PORT% --bind 127.0.0.1
echo.
echo Il server si e' fermato. Se vedi un errore qui sopra, copialo e mandamelo.
pause
```

### Code of `avvia-chat-rete.bat` (PC + phone)

```bat
@echo off
setlocal
title Offline Character Chat (rete)
cd /d "%~dp0"

if not exist "server.py" (
  echo Non trovo server.py in questa cartella.
  pause
  exit /b 1
)
if not exist "offline-character-chat.html" (
  echo Non trovo offline-character-chat.html in questa cartella.
  pause
  exit /b 1
)

set "PORT=8000"
netstat -ano | findstr /R /C:":%PORT% .*0.0.0.0:0" >nul 2>&1
if %errorlevel%==0 (
  echo La porta %PORT% e' gia' in uso: un altro server e' attivo.
  echo Chiudi la sua finestra e riprova.
  pause
  exit /b 1
)

set "PY="
where py >nul 2>&1 && set "PY=py"
if not defined PY where python >nul 2>&1 && set "PY=python"
if not defined PY (
  echo Python non trovato. Installalo da https://www.python.org/downloads/
  echo e spunta "Add Python to PATH" durante l'installazione.
  pause
  exit /b 1
)

echo Se Windows chiede l'accesso di rete, consenti le reti PRIVATE.
echo.
start "" /min cmd /c "ping -n 3 127.0.0.1 >nul & start http://localhost:%PORT%/"
%PY% server.py --lan %PORT%
echo.
echo Il server si e' fermato. Se vedi un errore qui sopra, copialo e mandamelo.
pause
```
