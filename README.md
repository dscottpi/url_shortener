### URL shortener

A simple URL shortener built on Flask.

For every new URL submitted, it generates an ID akin to [Twitter snowflake](https://blog.twitter.com/engineering/en_us/a/2010/announcing-snowflake) and encodes it to [base62](https://en.wikipedia.org/wiki/Base62).

This project was just for learning as I was most interested in implementing a Snowflake ID generator and base62 converter. The rest of the code is.. not my best.

I also haven't implemented anything that would allow you to scale up to multiple machines (which is the main use case for using something like Snowflake in the first place) but in theory the Snowflake implementation wouldn't have to change for that to be possible.
