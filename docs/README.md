# Slack team location planner

We created a simple solution for getting a overview for planning when people in the team are coming into the office, without the need to introduce any new tools or complex 3rd-party slack applications.

This python script posts a message in multiple slack channels, and responds to the same message with 5 emojies that represent the weekdays.

The application is self-hosted and uses a Slack bot token, cron jobs can be created from CI tools like Github Actions / CircleCI Cron, run as a Kubernetes cron job or just be run locallly with python/docker.

<img src="https://user-images.githubusercontent.com/29174850/172590122-1ad3a908-efa2-4d91-92f1-d4df5f733e4f.png" width="250">

![Screenshot from 2022-06-08 09-03-23](https://user-images.githubusercontent.com/29174850/172578268-302858d3-76cf-4b21-99cd-ac9fc89e2201.png)

## Onbarding

To add a new channel:

- Type `/invite atoffice` in the channel to grant permissions to the bot.
- Create a new PR.
- Enter channel name in `channels.txt`, create commit.
- Merge PR to main.

## Slack Bot configuration

Create a new Slack app, customize it as you prefer.

The bot requires the following **bot token scopes**:

- `chat:write`
- `reactions:write`

Install the bot to you slack organization after setting permissions, you will get a new slack bot token afterwards.

## Using docker

You need two things, a `.txt` file containing name of the slack channels and a environment variable for the bot token.

The .txt file should be mounted to `/app/channels.txt` in the docker container.

Set the `SLACK_BOT_TOKEN` environment variable with the token you got when creating the slack app.
