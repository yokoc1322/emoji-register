# emoji-register

emoji-register make be able to register Emoji by slash command.
It can register Moji-Emoji(like https://emoji-gen.ninja/) and normal Emoji.

## How to Use

### Configure slash command in slack

### Run emoji-register-server

```bash
docker build -t emoji-register .
docker run \
    -p <bind port ex. 8080:80>
    -e SLACK_APP_TOKEN=<slash command token> \
    -e PORT=<port ex. 80> \
    -e SLACK_COOKIE=<Please refer https://github.com/smashwilson/slack-emojinator> \
    -e SLACK_TEAM=<slack team name> \
    emoji-register
```

NOTE: The container is to be able to access from external network.

### Execute slach command

For example:

- `/emoji-register あいう aiu` (Moji-Emoji named aiu)
- `/emoji-register あい\nう aiu` (Moji-Emoji contain newline named aiu)
- `/emoji-register https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png github` (normal Emoji named github)
