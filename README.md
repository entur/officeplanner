# Slack team location planner

![pylint]()

We created a simple solution for getting a overview for planning when people in the team are coming into the office, without the need to introduce any new tools or complex 3rd-party slack applications.

This python script posts a message in multiple slack channels, and responds to the same message with 5 emojies that represent the weekdays.

The application is self-hosted and uses a Slack bot token, cron jobs can be created from CI tools like Github Actions / CircleCI Cron, run as a Kubernetes cron job or just be run locallly with python/docker.

![Slack team location planner](https://user-images.githubusercontent.com/29174850/172590122-1ad3a908-efa2-4d91-92f1-d4df5f733e4f.png)

![Screenshot from 2022-06-08 09-03-23](https://user-images.githubusercontent.com/29174850/172578268-302858d3-76cf-4b21-99cd-ac9fc89e2201.png)

## Onbarding

To add a new channel:

- Type `/invite atoffice` in the channel to grant permissions to the bot.
- Create a new PR.
- Enter channel name in `channels.txt`, create commit.
- Merge PR to main.

## Slack Bot configuration

You need to create a Slack app yourself at <https://api.slack.com/apps/>

Create a new Slack app, customize it as you prefer.

The bot requires the following **bot token scopes**:

- `chat:write`
- `reactions:write`

Install the bot to you slack organization after setting permissions, you will get a new slack bot token afterwards.

## Using the script

As a pre-requsite, you'll need to have 5 custom emojies representing each day in your slack organization. Without the emojies defined in the list below, the script will fail.

- `:monday:`
- `:tuesday:`
- `:wednesday:`
- `:thursday:`
- `:friday:`

> Example emojies can be found under the `examples/` folder.

To run the script you need two things, a `.txt` file containing name of the slack channels and a environment variable for the bot token.

### Python

If you are using python, then a `channels.txt` file should exist next to the `officeplanner.py` script and the `SLACK_BOT_TOKEN` must be populated in the same shell as the one running python.

### Docker

The latest docker image is available on github packages, and is updated when a PR is pushed to the `main` branch.

```yaml
ghcr.io/entur/officeplanner:main
```

Mount a `.txt` file to `/app/channels.txt` in the docker container.

Populate a `SLACK_BOT_TOKEN` environment variable with the token you got when creating the slack app.

## Bump versions manually

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install pip-tools
pip-sync
# bump versions in the requirements.in file
pip-compile
# test install the new versions
pip-sync
```
