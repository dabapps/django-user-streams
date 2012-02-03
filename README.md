# django-user-stream

**Simple, fast user news feeds for Django**

**Author:** Jamie Matthews. [Follow me on Twitter](http://twitter.com/j4mie).

## Changelog

#### 0.1.0

* Initial release.

## Overview

An app for creating *news feeds* (also known as *activity streams*) for users,
notifying them of activity happening around your site. Optimised for speed,
pluggability and simplicity.

News feed items are stored as a string and a timestamp. You can't store any
additional metadata about the stream items, such as generic foreign keys to and
`Actor` or a `Target`. You just store the item content as plain text (or HTML).
If you need links to other objects, just insert an `<a>` tag.

## Installation

You can install django-user-stream from PyPI:

    pip install django-user-stream

Add `user_streams` to your `INSTALLED_APPS` setting. You also need a *backend*,
which defines how your streams are stored. These are described below.

```python
INSTALLED_APPS = [
    ...
    'user_streams',
    'user_streams.backends.single_table',
    ...
]

USER_STREAM_BACKEND = 'user_streams.backends.single_table.SingleTableDatabaseBackend'
```

Finally, if you're using a backend that stores stream items using Django's model
layer, run `manage.py syncdb` to create the necessary database tables.

## API

### Adding items to streams

To create a stream item:

```python
import user_streams

user = User.objects.get(username='jamie')
user_streams.add_stream_item(user, 'This is the contents of the stream item')
```

The first argument to `add_stream_item` can be a single `User` instance, or a queryset
representing multiple users. In the latter case, the message you supply is added
to the stream of each user in the queryset.

```python
import user_streams

user_streams.add_stream_item(User.objects.all(), 'Broadcast message to all users')
```

### Getting the stream for a user

To retrieve the stream items for a user:

```python
import user_streams

user = User.objects.get(username='jamie')
items = user_streams.get_stream_items(user)
```

This will return an iterable of objects, each of which is guaranteed to have two
properties: `created_at`, which will be a `datetime.datetime` instance
representing the creation timestamp of the message, and `content`, which will
contain the contents of the message as a string. The objects will be ordered by
their `created_at` field, with the most recent first. The iterable that is
returned will be *lazy*, meaning that you can slice it (and pass it to a Django
`Paginator` object) without loading all of the items from the database.

### Backends

Stream storage is abstracted into `Backend` classes. Three are shipped with
`django-user-streams`, Each backend is kept in a separate reusable app, which
must be added to `INSTALLED_APPS` separately to the main `user_streams` app. This
is to ensure that only the database tables required for each backend are created
(assuming you are using a backend that stores data through Django's model
 layer).

Which backend you choose depends on the scale of your application, as well as
your expected usage patterns.

#### SingleTableDatabaseBackend

`user_streams.backends.single_table.SingleTableDatabaseBackend`

The simplest backend. Your stream items are stored in a single database table,
consisting of a foreign key to a `User` object, a `DateTimeField` timestamp, and
a `TextField` to store your message. Fetching a stream for a user should be
extremely fast, as no database joins are involved. The tradeoff is storage
space: If you send a message to multiple users, the message is stored multiple
times, once for each user. If you regularly broadcast messages to thousands of
users, you may find that the table gets very large.

#### ManyToManyDatabaseBackend

`user_streams.backends.many_to_many.ManyToManyDatabaseBackend`

This backend stores your messages in a table with a `ManyToManyField`
relationship to your `User` objects. Each message is only stored *once*, with a
row in the intermediate table for each recipient. This means you need much less
space for broadcast messages, but your queries may be slightly slower.

#### RedisBackend

`user_streams.backends.redis.RedisBackend`

Stores your messages in Redis sorted sets, one set for each user,  with a Unix
timestamp (the `created_at` attribute) as the score for each item. This approach
is described in more detail
[here](http://blog.waxman.me/how-to-build-a-fast-news-feed-in-redis). The
iterable returned by `get_stream_items` uses `ZREVRANGE` to retrieve each slice of the
feed, and `ZCARD` to get the complete size of the set of items. This backend
should be screamingly fast.

#### Writing your own backend

You can create your own backend to store messages in whatever data store suits
your application. Backends are simple classes which must implement two methods:

##### add_stream_item

`add_stream_item(self, users, content, created_at)`

`users` will be an *iterable* of `User` instances (you don't need to worry
about accepting a single instance - your backend method will always be called
with an iterable, which may be a list containing only one `User`.

`content` will be a string containing the stream message to store.

`created_at` will be a Python `datetime.datetime` object representing the
time at which the stream item was created.

##### get_stream_items

`get_stream_items(self, user)`

This method should return an iterable of messages for the given `User`, sorted
by timestamp with the newest first. Each item must be an object with two
attributes: `created_at` (which must be a Python `datetime.datetime` object)
and `content` (which must be a string containing the message contents).

While this method could simply return a `list` of messages, it's much more
efficient to assume that the list will be paginated in some way, and support
slicing and counting the objects on-demand, in whatever method your data store
supports. To do this, you should return an iterable object, overriding
`__getitem__` and `__len__`. See the implementation of `RedisBackend` for an
example.

## Alternatives

https://github.com/justquick/django-activity-stream

## Development

To contribute: fork the repository, make your changes, add some tests, commit,
push to a feature branch, and open a pull request.

### How to run the tests

Rediset is tested with [nose](http://nose.readthedocs.org). Clone the repository,
create a virtualenv, then run `pip install -r requirements.txt`. Then, simply type
`nosetests` to find and run all the tests.

## (Un)license

This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or distribute this
software, either in source code form or as a compiled binary, for any purpose,
commercial or non-commercial, and by any means.

In jurisdictions that recognize copyright laws, the author or authors of this
software dedicate any and all copyright interest in the software to the public
domain. We make this dedication for the benefit of the public at large and to
the detriment of our heirs and successors. We intend this dedication to be an
overt act of relinquishment in perpetuity of all present and future rights to
this software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS BE
LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
