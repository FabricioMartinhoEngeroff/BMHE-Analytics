PS C:\Insights e-commerce\BMHE-Analytics-Backend> .\.venv\Scripts\Activate       
>> python -m uvicorn mcp_backend.app.main:app --reload --host 0.0.0.0 --port 8000
INFO:     Will watch for changes in these directories: ['C:\\Insights e-commerce\\BMHE-Analytics-Backend']
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
INFO:     Started reloader process [13512] using WatchFiles
Process SpawnProcess-1:
Traceback (most recent call last):
  File "C:\Python313\Lib\multiprocessing\process.py", line 313, in _bootstrap
    self.run()
    ~~~~~~~~^^
  File "C:\Python313\Lib\multiprocessing\process.py", line 108, in run
    self._target(*self._args, **self._kwargs)
    ~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\_subprocess.py", line 80, in subprocess_started
    target(sockets=sockets)
    ~~~~~~^^^^^^^^^^^^^^^^^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\server.py", line 66, in run
    return asyncio.run(self.serve(sockets=sockets))
           ~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "C:\Python313\Lib\asyncio\runners.py", line 195, in run
    return runner.run(main)
           ~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\asyncio\runners.py", line 118, in run
    return self._loop.run_until_complete(task)
           ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^
  File "C:\Python313\Lib\asyncio\base_events.py", line 719, in run_until_complete
    return future.result()
           ~~~~~~~~~~~~~^^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\server.py", line 70, in serve
    await self._serve(sockets)
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\server.py", line 77, in _serve
    config.load()
    ~~~~~~~~~~~^^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\config.py", line 435, in load
    self.loaded_app = import_from_string(self.app)
                      ~~~~~~~~~~~~~~~~~~^^^^^^^^^^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\uvicorn\importer.py", line 19, in import_from_string
    module = importlib.import_module(module_str)
  File "C:\Python313\Lib\importlib\__init__.py", line 88, in import_module
    return _bootstrap._gcd_import(name[level:], package, level)
           ~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "<frozen importlib._bootstrap>", line 1387, in _gcd_import
  File "<frozen importlib._bootstrap>", line 1360, in _find_and_load
  File "<frozen importlib._bootstrap>", line 1331, in _find_and_load_unlocked
  File "<frozen importlib._bootstrap>", line 935, in _load_unlocked
  File "<frozen importlib._bootstrap_external>", line 1026, in exec_module
  File "<frozen importlib._bootstrap>", line 488, in _call_with_frames_removed
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\mcp_backend\app\main.py", line 12, in <module>
    settings = get_settings()
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\mcp_backend\app\config\settings.py", line 34, in get_settings
    return Settings()
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\pydantic_settings\main.py", line 176, in __init__
    super().__init__(
    ~~~~~~~~~~~~~~~~^
        **__pydantic_self__._settings_build_values(
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    ...<26 lines>...
        )
        ^
    )
    ^
  File "C:\Insights e-commerce\BMHE-Analytics-Backend\.venv\Lib\site-packages\pydantic\main.py", line 253, in __init__
    validated_self = self.__pydantic_validator__.validate_python(data, self_instance=self)
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
DATABASE_URL
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing
SECRET_KEY
  Field required [type=missing, input_value={}, input_type=dict]
    For further information visit https://errors.pydantic.dev/2.11/v/missing