# ADR-0007: Core API as Protobuf, served as gRPC and Connect-JSON over mutual TLS

**Status:** Accepted · **Date:** 2026-11-25

## Context

[ADR-0001](0001-core-api-only.md) makes the Core API (`steelcore.v1`) the only way into the core. Until now it was an in-process Rust interface. Several providers will use it: steelnet for Steelbound players today, Brainbox and Insignia later. They run different stacks. steelnet, for example, is Python with the standard library only, and it should stay that way. The core also owns players, identities and display names (gamertags), and it has to enforce their uniqueness across all providers. A provider must never be able to act for another provider's users.

## Decision

1. **One contract:** `steelcore.v1` is defined in Protobuf ([`proto/steelcore/v1`](https://github.com/Greevee-Lab/sbcampaign/tree/master/proto/steelcore/v1) in the fork). It starts with `IdentityService` (`ResolveIdentity`), `PlayerService` (`GetPlayer`, `CheckDisplayName`, `SetDisplayName`) and `AdminService` (`SetIdentitySuspended`). Campaign commands follow later as further services in the same package. Fields are only ever added. Incompatible changes go to `steelcore.v2`.
2. **Two equal bindings on one port:**
   - **gRPC** (HTTP/2) for server stacks that have gRPC anyway.
   - **Connect-JSON** (the unary Connect protocol): `POST /steelcore.v1.<Service>/<Method>` with the proto3 JSON mapping. A client only needs HTTPS and JSON.

   Both bindings call the same server functions. A test runs the same call sequence through both and requires identical results.
3. **Mutual TLS 1.3 with a steelcore CA:** each provider access has its own client certificate. The server accepts only certificates issued by its own CA, *and* only if the certificate's SHA-256 fingerprint is configured as an access. Renewal and revocation are configuration changes, so no CRL is needed. The CA key stays offline with the operator.
4. **Access = provider + scopes + rate limit.** The provider of an identity always comes from the access, never from the request. Scopes: `identity:write`, `profile:write`, `read:public`, `admin`. A statistics service gets only `read:public`.
5. **Writes** carry an idempotency key, and every write leaves an audit row: access, provider, method, identity or player, and outcome, but never request contents.
6. **steelnet** uses Connect-JSON with Python's `http.client` and `ssl`. It needs no new dependency and no virtual environment on the server.

## Consequences

- **+** One contract for every provider. Brainbox and Insignia can connect with any gRPC or HTTP library, without a special path.
- **+** No library or virtual environment is added to steelnet. The Python client is one small module.
- **+** A compromised provider can only act within its own scopes, for its own users, and under its rate limit. It can never act for another provider's players, read their identities, or touch the database.
- **+** No `protoc` is needed to build. The server parses the `.proto` files in Rust.
- **−** Two bindings to keep equal. This is mitigated because both share one implementation and one test.
- **−** The certificate lifecycle is manual: renewal about once a year per access.

## Alternatives considered

- **`grpcio` in a virtual environment for steelnet:** it works, but adds a large native dependency and extra memory to a small service, plus wheel compatibility on server upgrades.
- **gRPC-JSON transcoding with custom REST paths:** needs per-method HTTP annotations and a second set of routes to maintain. Connect-JSON maps every method by name.
- **A separate hand-written REST API:** this would be two contracts that drift apart. Rejected by "one source of truth".
- **API keys instead of client certificates:** simpler, but a leaked key works from anywhere and is harder to scope to one host. mTLS binds the access to a key that never leaves the provider's server.
