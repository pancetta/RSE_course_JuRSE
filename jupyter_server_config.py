# Configuration for Jupyter Server with Jupytext syncing.
#
# This file enables bidirectional syncing between the Jupytext .py source files
# and the generated .ipynb notebook files. When enabled:
#   - Opening a notebook in Jupyter reads from the paired .py file
#   - Saving a notebook writes to both .ipynb and .py files
#   - The .py source files always stay up-to-date with your edits
#
# This also helps reduce spurious "Kernel does not exist" (404) warnings
# because notebooks are loaded fresh from the .py files each session,
# rather than restoring a stale notebook state.
#
# Usage:
#   Use 'make start-notebook' to launch Jupyter with this configuration, or
#   copy this file to your Jupyter config directory (run: jupyter --config-dir)
#   and restart Jupyter.

c.ServerApp.contents_manager_class = "jupytext.TextFileContentsManager"  # noqa: F821
# Note: `c` is Jupyter's configuration object, automatically injected when this
# file is loaded by the Jupyter server. It does not need to be imported.
