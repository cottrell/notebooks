# Error with typer

Argh works, typer has trouble with star arguments.

```shell
$ ./example_with_argh.py a b
a ('b',)
$ ./example_with_argh.py a b c
a ('b', 'c')
$ ./example.py a b
Traceback (most recent call last):
  File "./example.py", line 8, in <module>
    typer.run(this)
  File "/home/cottrell/dev/typer/typer/main.py", line 856, in run
    app()
  File "/home/cottrell/dev/typer/typer/main.py", line 214, in __call__
    return get_command(self)(*args, **kwargs)
  File "/home/cottrell/anaconda3/envs/38/lib/python3.8/site-packages/click/core.py", line 829, in __call__
    return self.main(*args, **kwargs)
  File "/home/cottrell/anaconda3/envs/38/lib/python3.8/site-packages/click/core.py", line 782, in main
    rv = self.invoke(ctx)
  File "/home/cottrell/anaconda3/envs/38/lib/python3.8/site-packages/click/core.py", line 1066, in invoke
    return ctx.invoke(self.callback, **ctx.params)
  File "/home/cottrell/anaconda3/envs/38/lib/python3.8/site-packages/click/core.py", line 610, in invoke
    return callback(*args, **kwargs)
  File "/home/cottrell/dev/typer/typer/main.py", line 497, in wrapper
    return callback(**use_params)  # type: ignore
TypeError: this() got an unexpected keyword argument 'b'
$ ./example.py a b c
Usage: example.py [OPTIONS] A B
Try 'example.py --help' for help.

Error: Got unexpected extra argument (c)
```

