JSON
====

JSON is a data serialization format which is easy
for humans to read and write.

Here is an example of JSON code:

.. code-block:: json

    {
        "my_key": "my_string_value",
        "another_key": true,
        "hello": [
            "value1", 2, false, null
        ]
    }

As you can see, it is similar to Python dictionaries and
lists. It is also very intuitive to understand.

The JSON submodule in East can be accessed with

.. code-block: python

    import east
    east.json

We recommend NOT importing json from east ``from east import json``,
because that may introduce name collisions with the builtin json
module.
