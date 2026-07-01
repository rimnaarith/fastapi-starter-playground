This is one of the most confusing parts of FastAPI for beginners, because it combines **two Python features**:

1. `async with`
2. `yield`

Let's learn them separately first.

---

# Part 1: What is `async with`?

Suppose you open a file.

Without `with`:

```python
file = open("hello.txt")

content = file.read()

file.close()
```

Notice you have to remember to call:

```python
file.close()
```

What if an exception happens before `close()`?

```python
file = open("hello.txt")

raise Exception("Oops!")

file.close()    # Never reached
```

The file stays open.

---

Using `with`:

```python
with open("hello.txt") as file:
    content = file.read()
```

Python automatically does:

```
Open file
      │
Read file
      │
Close file
```

Even if an exception happens.

---

## `async with` is the same idea

Instead of a file, we're managing a **database session**.

```python
async with AsyncSessionLocal() as session:
```

means

```
Create Session
      │
Use Session
      │
Automatically Close Session
```

You never call:

```python
await session.close()
```

because `async with` does it for you.

---

# Why "async"?

Database operations are asynchronous.

Opening/closing a database connection may involve waiting.

So instead of:

```python
with
```

we use

```python
async with
```

because SQLAlchemy's `AsyncSession` supports asynchronous context management.

---

# Part 2: What does `yield` do?

Normally a function returns once.

```python
def hello():
    return "Hi"

print(hello())
```

Output:

```
Hi
```

After `return`, the function is finished forever.

---

`yield` is different.

Imagine this:

```python
def numbers():
    yield 1
    yield 2
    yield 3
```

Calling it:

```python
nums = numbers()
```

does **not** run the whole function.

It creates a generator.

```
numbers()
     │
Generator object
```

Then:

```python
next(nums)
```

Output:

```
1
```

Call again:

```python
next(nums)
```

Output:

```
2
```

Again:

```
3
```

The function pauses at each `yield`.

---

Think of `yield` as:

```
Run
Pause
Resume
Pause
Resume
```

instead of

```
Run
Finish
```

---

# How FastAPI uses `yield`

Your code:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

looks small, but FastAPI treats it specially.

Imagine this endpoint:

```python
@app.get("/users")
async def users(
    db: AsyncSession = Depends(get_db)
):
    ...
```

When a request comes in:

```
Client
   │
   ▼
FastAPI
   │
Call get_db()
```

Inside `get_db`:

```
Create Session
```

Then:

```
yield session
```

At this point, the function **pauses**.

The session is handed to your endpoint.

```
get_db()

Create Session
      │
yield session
      │
PAUSED
```

Now your endpoint runs.

```
Endpoint

db.execute(...)
db.commit(...)
return response
```

After the endpoint finishes...

FastAPI resumes `get_db()`.

```
yield session
      │
Resume
```

Now execution reaches the end of the `async with` block.

Leaving the `async with` block automatically closes the session.

```
Close Session
```

---

# Timeline

```
Request starts
      │
      ▼
Create Session
      │
      ▼
yield session
      │
      ▼
Endpoint runs
      │
      ▼
Endpoint returns
      │
      ▼
Resume get_db()
      │
      ▼
Session closes
      │
      ▼
Request ends
```

---

# Why not use `return`?

Imagine:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        return session
```

What happens?

```
Create Session
Return Session
Exit async with
Session Closed
```

Now your endpoint receives a **closed session**.

```
Endpoint

db.execute(...)
```

💥 Error!

The session is already closed.

---

With `yield`:

```
Create Session
      │
Give Session
      │
Endpoint uses it
      │
Close Session
```

The session stays alive while the endpoint is running.

---

# FastAPI is secretly doing something like this

Internally, it behaves conceptually like:

```python
generator = get_db()

db = await generator.__anext__()   # Runs until yield

try:
    response = await endpoint(db)
finally:
    try:
        await generator.__anext__()  # Continue after yield
    except StopAsyncIteration:
        pass
```

You don't write this yourself—FastAPI handles it for you.

---

# Why use `yield`?

Because it lets you define **setup** and **cleanup** in one place.

```python
async def get_db():
    # Setup
    session = create_session()

    try:
        # Give it to the endpoint
        yield session
    finally:
        # Cleanup
        await session.close()
```

The `async with` version is just a cleaner way to express the same pattern:

```python
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session
```

This is why `yield` is the recommended approach for FastAPI dependencies that need cleanup: it guarantees resources like database sessions, files, or network connections remain available while your endpoint runs and are released automatically afterward, even if an exception occurs.
