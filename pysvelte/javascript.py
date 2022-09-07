import stat
import subprocess
import threading

from .vis_paths import NODE_ROOT, COMPONENTS_DIST, INTERNAL_COMPONENTS_SRC, Path


def mtime(path: Path):
    try:
        st = path.stat()
    except FileNotFoundError:
        return 0
    if stat.S_ISDIR(st.st_mode):
        fs = list(path.rglob("*"))
        if fs:
            return max(mtime(f) for f in fs)
        else:
            return 0
    else:
        return st.st_mtime


def is_npm_install_necessary():
    """Check if npm dependencies are out of date or missing."""
    if not NODE_ROOT / "node_modules".exists():
        return True
    return mtime(NODE_ROOT / "node_modules") < mtime(NODE_ROOT / "package.json")


def install_if_necessary():
    """Install npm modules if they're out of date or missing."""
    if is_npm_install_necessary():
        print("Installing node.js dependencies...")
        subprocess.check_call(["npm", "--prefix", str(NODE_ROOT), "ci"])


# TODO: this looks like it's intended to prevent duplicate concurrent webpack builds
# but I'm unsure/unconvinced it actually does this.
# * If we have several entirely different notebook processes this lock won't stop them interfering
# * If we have one notebook/IPython process, the GIL means only one thread runs at once and notebook
#   cells run serially and as far as I can tell on a single thread
# So I think this lock can only cause deadlock (when a rebuild is interrupted) and won't catch actual problems
vis_build_lock = threading.Lock()


def webpack_if_necessary(paths=None):
    """Use webpack to rebuild visualization components if missing or out of date.

    Args:
      paths: Assets to build if necesary. If None (the default) we build all.
    """
    with vis_build_lock:
        # TODO: this assumes a fixed SRC path
        dists = [COMPONENTS_DIST / p for p in paths] or [COMPONENTS_DIST]
        stale = any(
            mtime(dist) < mtime(INTERNAL_COMPONENTS_SRC) or mtime(dist) < mtime(NODE_ROOT / "package.json")
            for dist in dists
        )
        if stale:
            print("pysvelte components appear to be unbuilt or stale")
            install_if_necessary()
            print("Building pysvelte components with webpack...")
            if paths:
                entries = [p.split("/")[-1].replace(".js", "") for p in paths]
                entries = ",".join(entries)
                env_flag = [f"--env=entry={entries}"]
            else:
                env_flag = []
            subprocess.check_call(["npx", "webpack"] + env_flag, cwd=str(NODE_ROOT))


def get_src_path(name):
    if (f := INTERNAL_COMPONENTS_SRC / f"{name}.svelte").exists():
        return f
    if (f := INTERNAL_COMPONENTS_SRC / f"{name}/main.svelte").exists():
        return f


def get_dist_path(name):
    return COMPONENTS_DIST / f"{name}.js"


def load_dist_path(path):
    webpack_if_necessary([path])
    dev_path = COMPONENTS_DIST / path
    if not dev_path.exists():
        msg = f"Could not find the built file '{path}' "
        raise Exception(msg)
    with dev_path.open() as f:
        return f.read()


def get_script_tag(path, dev_host=None):
    if not dev_host:
        return f"<script>{load_dist_path(path)}</script>"
    else:
        dev_url = dev_host + ('/' if dev_host[-1] != '/' else '') + path
        return f"<script src='{dev_url(dev_host, path)}'></script>"


def get_script_tags(paths, dev_host=None) -> str:
    """Get html <script> tags to load the visualizations at paths.

    Args:
      paths: paths to assets to be built, assumed to be in DIST.
      dev_host: If this value is set (not None), we are assumed to be
        in "dev mode". Rather than inlining the javascript, we try to
        load it from a url based on dev_host.
    """
    if dev_host is None:
        # Although the get_script_tag() below would also trigger builds,
        # doing it like this builds all needed assets in one pass which is
        # significantly faster.
        webpack_if_necessary(paths)
    tags = [get_script_tag(path, dev_host=dev_host) for path in paths]
    return "\n".join(tags)
