# Native loader follow-up — read-only public documentation

Narrow question: is a publicly documented, supported native loader already adopted
here that supplies the required post-roll/pre-removal callback in Build 42.21?
No such project dependency/callback was established in this pass. This is not a
claim that a Java bridge is technically impossible; it is the remaining loader,
build compatibility, interface and dedicated-runtime validation work.

The installed FadedJavaLoader/plugins directory is empty. Public primary-site
metadata confirms a Java-loader ecosystem, but the reviewed page does not establish
the necessary plugin/hook interface. Its downloads require an access/confidentiality
agreement; no agreement was accepted, protected download accessed, installer run
or third-party implementation inspected. Public source:
[Faded Mods](https://fadedmods.com/).

An alternative primary API reference, [PZHook](https://github.com/Olipro/PZHook),
documents Java mod loading, an agent/main-entry installation path, server mode
and method interception. It also documents competing hook ownership. Those public
API statements do not verify a compatible Build 42.21 mid-method injection at this
mod's required seam. No example source or implementation was copied, dependency
downloaded/bundled, launcher changed or loader installed.

SOURCE CODE COPIED: NO
IMPLEMENTATION DERIVED FROM REFERENCE: NO

Design consequence: a narrow original native bridge remains appropriate, as allowed
by docs/JAVA_DEVELOPMENT_POLICY.md. Before enabling gameplay, adopt and verify an
exact loader/public interface (or an original reproducible instrumentation loader),
pin supported builds, establish hook conflict behavior and client/server placement,
verify license/redistribution decisions, then compile/offline-test the bridge and
obtain actual dedicated evidence. Do not infer readiness from a website listing.
