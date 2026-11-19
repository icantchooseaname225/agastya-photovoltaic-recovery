# Environment setup

The current workspace was run on Windows with CPython 3.14.4, PowerShell 7.6.5 and Node.js 24.19.0. Python/Node support packages were available in the Codex desktop bundled runtime. Those bundled absolute paths are machine-specific; the project does not include a portable environment lockfile.

For the existing accounting scripts, open PowerShell, go to `Agastya Physics Simulation\Research Phase B-C`, and check `python --version`. It should report Python 3.14.x. The scripts use the standard library; do not install extra packages for them.

For presentation rebuilds, use the bundled Node runtime and set `NODE_PATH` to the runtime's `node_modules` folder before running `05_Presentation\Working_Drafts\build_agastya_presentations.js`. In this workspace the module path is `%USERPROFILE%\.cache\codex-runtimes\codex-primary-runtime\dependencies\node\node_modules`; paths are machine-specific. If the package is unavailable on another computer, stop and document that limitation rather than changing the final deck by hand without a record.

No external solver or laboratory software is part of the verified environment. Do not install paid or hazardous-process software/equipment without a justified study design and approval.
