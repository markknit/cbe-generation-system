# Running the Lesson3 test suite

Quick setup note so you can run all four test tiers locally. Lesson3's own
`AGENTS.md` (in the repo root) is the canonical source if anything below is
unclear or out of date — this note is a condensed path through it, not a
replacement for it.

**Repo:** https://github.com/james-beep-boop/Lesson3 (public — just clone it)

---

## Prerequisites

- **Docker + Docker Compose.** Nearly everything below runs inside a pinned
  container, so your host's Node version doesn't matter for `test:unit`,
  `test:int`, or `test:http`.
- **Git**, for the clone.
- **Playwright's browser**, for `test:e2e` only — one-time:
  ```bash
  cd app && npx playwright install chromium
  ```

---

## The four tiers, and what "all of them" actually means

There is no single `npm run test:all`. Covering everything means running
**two** commands:

```bash
npm run test:rock   # = test:unit + test:int + test:http
npm run test:e2e    # browser flows, run separately
```

## 1. `test:unit` — easiest, no database

Pure logic, DB-free. From the repo root:

```bash
scripts/in-deps.sh --network none -- npm run test:unit
```

## 2. `test:int` — needs a disposable Postgres stack

Don't point this at any "real" dev database — it has its own isolated,
throwaway stack for exactly this reason. Run from the **repo root**
(the first line matters — a few past mistakes came from running this
from inside `app/`, which silently creates a dead `app/app/node_modules`
and produces a build with zero working routes):

```bash
ROOT=$(git rev-parse --show-toplevel) && cd "$ROOT"

# 1. stand up the isolated stack (its own volumes/network — never touches
#    any seeded dev database)
docker compose -p lesson3-ci-probe up -d --build

# 2. create the test DB inside THAT stack's postgres
docker compose -p lesson3-ci-probe exec -T postgres psql -U lesson3 -d postgres \
  -c "CREATE DATABASE lesson3_test;"

# 3. point the tracked app/test.env at it (you'll restore this in step 5)
PW=$(grep -E '^POSTGRES_PASSWORD=' "$ROOT/.env" | cut -d= -f2-)
sed -i '' -E "s#^DATABASE_URI=.*#DATABASE_URI=postgres://lesson3:${PW}@postgres:5432/lesson3_test#" "$ROOT/app/test.env"

# 4. run (NODE_ENV=test is required here — NOT "development"; the latter
#    turns on schema auto-push inside the test process and deadlocks
#    against the app's own job-queue transactions)
scripts/in-deps.sh --network lesson3-ci-probe_default \
  --env-file "$ROOT/.env" -e NODE_ENV=test -- npm run test:int

# 5. restore the tracked file and prove it's clean
git -C "$ROOT" checkout -- app/test.env && git -C "$ROOT" diff --exit-code -- app/test.env
```

Teardown when done — **always include `-p`**, or you risk destroying a
real seeded database instead of this throwaway one:

```bash
docker compose -p lesson3-ci-probe down -v --remove-orphans
```

## 3. `test:http` — same disposable stack, plus the app itself running

`test:http` drives the real app over HTTP, so it reuses the same
`lesson3-ci-probe` stack from step 2 (never the seeded dev database — the
fixture setup in these specs does a destructive namespace sweep and will
happily wipe real data if pointed at it) and additionally needs the app
running inside that stack, reachable as `E2E_BASE_URL=http://app:3000`.

I don't have the exact extra docker-compose invocation for bringing the
`app` service up confirmed firsthand — rather than guess at it, check
`AGENTS.md`'s Commands section and `docs/DECISIONS.md`'s
**"2026-08-18 — http/e2e fixtures go to the probe stack, never the seeded
dev database"** entry, which spells out why and has the surrounding
detail (e.g. `vitest.http.config.mts` passes `--env-file .env` for
production/migrate mode — same `NODE_ENV` reasoning as `test:int` above).

## 4. `test:e2e` — Playwright, same "never the seeded DB" rule applies

By default, `playwright.config.ts` auto-starts `npm run dev` for you against
`localhost:3000` if `E2E_BASE_URL` isn't set — convenient, but per the same
`DECISIONS.md` entry above, e2e's fixture setup must run against a
disposable stack, not your normal seeded local dev database (same
destructive-sweep risk as `test:http`). Set `E2E_BASE_URL` to point at an
app instance backed by the `lesson3-ci-probe` stack rather than relying on
the auto-started default, unless you're fine with that run purging fixture
data in whatever database it lands on.

---

## tl;dr safety notes

- Always include `-p lesson3-ci-probe` on compose teardown.
- `NODE_ENV=test`, never `development`, for any test container.
- Never point `test:http`/`test:e2e` at the seeded local dev database.
- Run `test:int` from the repo root, not from inside `app/`.
