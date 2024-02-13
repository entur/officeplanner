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

You need to create a Slack app yourself at https://api.slack.com/apps/

Create a new Slack app, customize it as you prefer.

The bot requires the following **bot token scopes**:

- `chat:write`
- `reactions:write`

Install the bot to you slack organization after setting permissions, you will get a new slack bot token afterwards.

Populate a `SLACK_BOT_TOKEN` environment variable with the token you got when creating the slack app.

## Using the script

As a pre-requsite, you'll need to have 5 custom emojies representing each day in your slack organization. Without the emojies defined in the list below, the script will fail.

- `:monday:`
- `:tuesday:`
- `:wednesday:`
- `:thursday:`
- `:friday:`

> Example emojies can be found under the `examples/` folder.

### Slack channel mode

There are two modes available, which can be changed using the `MODE` environment variable:

  - `file` (default)
    - Expects a `.txt` file with channel names, iterates over each line in file.
    - Default is `/app/channels.txt`, can be overridden with the `CHANNELS_FILE` environment variable.
  - `single`
    - Sends the message to a single slack channel.
    - Enter the slack channel (with # prefix) in the `SLACK_CHANNEL` environment variable.

#### File mode

If you are using the default File mode, then a `channels.txt` file must exist next to the `officeplanner.py` script, or mounted as a Volume in Docker.

### Docker

The latest docker image is available on github packages, and is updated when a PR is pushed to the `main` branch.

```
ghcr.io/entur/officeplanner:main
```

Mount a `.txt` file to `/app/channels.txt` in the docker container.

### Kubernetes Cronjob

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: office-planner
spec:
  schedule: 0 9 * * 1
  concurrencyPolicy: Forbid
  jobTemplate:
    spec:
      activeDeadlineSeconds: 3600
      backoffLimit: 100
      template:
        spec:
          restartPolicy: OnFailure
          containers:
            - name: office-planner
              image: office-planner:v1.0.1
              env:
                - name: MODE
                  value: single
                - name: SLACK_CHANNEL
                  value: '#di-analyse'
                - name: TZ
                  value: Europe/Oslo
                - name: GREETING
                  valueFrom:
                    configMapKeyRef:
                      key: greeting
                      name: ap-office-planner
                - name: SLACK_BOT_TOKEN
                  valueFrom:
                    secretKeyRef:
                      key: SLACK_BOT_TOKEN
                      name: slack-token-office-planner
              livenessProbe:
                exec:
                  command:
                    - python3
                    - '--version' # TODO: add native health check
                failureThreshold: 3
                initialDelaySeconds: 30
                periodSeconds: 10
              resources:
                requests:
                  cpu: 25m
                  memory: 25Mi
                limits:
                  memory: 50Mi
              securityContext:
                allowPrivilegeEscalation: false
                capabilities:
                  drop:
                    - ALL
                readOnlyRootFilesystem: true
                runAsNonRoot: true
                runAsUser: 1000
          securityContext:
            fsGroup: 2000
```
