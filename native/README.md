# Native catch bridge development spike



Project Version: 0.5.0-dev.1



Original source, not a supported production dependency. Runtime decision:

REVISE. Read `../docs/NATIVE_BRIDGE_REPORT.md` before enabling it.



This uses the standard JVM `-javaagent` premain mechanism and Java 25's public

Class-File API. No FJL, PZHook, Byte Buddy, ASM or third-party loader is bundled.

No copied vanilla class or decompiled implementation is in the agent JAR.

JDK 25 is a build-only tool; the installed Azul 25.0.1 JRE executes the agent.

Neither toolchain is distributed with the mod. `build/` contains generated

classes, research copies and toolchains; never stage it as Workshop content.



Build, from the workspace, with your actual toolchain/game paths:



```powershell

./B47ANCEDEyewear/native/Build.ps1 -JdkHome <JDK25> -GameJar <projectzomboid.jar>

```



The three original Java source files compile against vanilla signatures; project

version and manifest are generated from root VERSION. Small direct javac/jar

build is appropriate for this dependency-free spike. No IDE or fixed absolute

path is required. Current build/test wrappers target Windows; Linux runtime

loading remains NOT TESTED, and Linux wrappers remain to be implemented if adopted.



Offline test (never starts the game):



```powershell

$pzPython = & ./tools/Resolve-HostTestPython.ps1

& $pzPython -B B47ANCEDEyewear/native/tests/run.py --jdk <JDK25> --game-jar <projectzomboid.jar> --runtime-java <game-jre-java.exe>

```



For an explicitly authorized isolated runtime experiment only, the JVM startup

argument is `-javaagent:<absolute-agent-jar>=fixture`. Without `=fixture` catches

are disabled. It must be supplied before game classes load. Dynamic attachment

and retransformation are unsupported. This repository does not modify launcher

JSON, installed JARs, server scripts or live mods. Existing class modification

before this agent causes exact-hash refusal; competing later transformers remain

an unproven compatibility risk. Use this agent alone in the first experiment.



`loader/CatchFixture.lua` is manually loaded into the SP/server Lua environment

only in the authorized isolated experiment. Select the exact worn compatible

`Base.Glasses` object as `B47ANCEDEyewearNativeFixtureItem`; nil disables it. The fixture
is read-only, session-local, grants no item and writes no save data. It is never

automatically loaded by the production mod. Existing tied ChanceToFall=0 eyewear

never reaches this hook; test an untied item with a positive native chance. Do

not change probability to fabricate a successful roll. Record real failures too.



The fixture global is not a client command or shipping API. A future production

callback needs a separate validated transaction adapter; this spike does not

make arbitrary Lua side effects rollback-safe. Incompatible agent registration

or callback errors preserve vanilla removal when the callback obeys its read-only

contract. A malformed startup option/unsupported JVM may fail before premain;

remove the option to recover. No Java agent can promise to recover JVM startup

failures that occur before it executes.



Technical constants (class hashes, method descriptors, audited local slots,

reentrancy guard, 32-line diagnostic limit) are compatibility/safety internals,

not gameplay settings. Fixture enablement is a development switch, not a hidden

alternative to future authoritative SandboxVars. Production sandbox behavior

is intentionally outside this gate.


Latest actual startup attempt and user-directed testing stop: see
`../docs/NATIVE_RUNTIME_VALIDATION.md`. Incompatible startup produced a duplicate-
class LinkageError; safe startup fallback is not established.

Current production proposal/commit candidate and remaining gates: ../docs/RETAINER_EXPANSION_IMPLEMENTATION.md. Fixture-only statements below describe historical spike behavior.
