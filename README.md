# Security Agent Test Repo

Throwaway repo used to test the Security Agent's GitHub App webhook + secret scanner.

Nothing sensitive here — `src/app_config.py` intentionally contains no secrets on `main`.
The test PR (see backend README / setup instructions) adds a fake secret on a branch to
verify the scanner picks it up.
