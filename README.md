HELP I CANT GET LOCAL LOGGING CONFIG, CHECK [this](https://github.com/koala9712/PyGrinder/blob/master/utils/Instance.py#L60-L79)

Hey!<br>
This is now one of my main projects, lookin forward to this!<br>
That being said, it is still not anywhere near usable, still in development.<br>

## Contributing
Glad you wanna, scroll down and check out my TODO list, now you know what to do!

## TODO:
This project was heavily inspired by [this one](https://github.com/dankgrinder/dankgrinder) and hopes to achieve at least what the original program has done.<br>
I.E. shifts, instances, config etc

This should also support more functions such as daily, weekly, monthly etc, as well as be compatible with new updates.<br>
(also alot for my own experience so yes)

Currently, need to make logging use local config, not global 💀<br>

## Errors:
    - 200: Ok! With content
    - 204: Ok! Without content
    - 400: InvalidResponse : bot did not reply with something I expected it to contain
    - 403: Account Bot Banned
    - 408: ResponeTimeout : did not reply in given response timeout :(
    - 412: NotJson : bot did not reply with json
    - 417: CommandNotSent : command was not sent
    - 422: NotHandled : something I did not forsee!
    - 424: InteractionFailed
    - 429: cooldown
    - 498: Account Discord Banned

## Config (Probably)

#### \_crime_mode:

    0: Preference from list, if not, random
    1: Preference from list, if not, cancel
    2: Random

#### \_search_mode:

    0: Preference from list, if not, random
    1: Preference from list, if not, cancel
    2: Random
