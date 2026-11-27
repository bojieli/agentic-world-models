"""Download the pinned inputs under the file names used by build.py."""
import argparse
from pathlib import Path
from shutil import copyfile
from huggingface_hub import HfApi, hf_hub_download

from build import RAW, REV_LB, REV_OH, REV_RB_META, REV_SMITH


def fetch(repo, rev, source, target, repo_type="dataset"):
    dest = Path(RAW) / target
    dest.parent.mkdir(parents=True, exist_ok=True)
    cached = hf_hub_download(repo_id=repo, filename=source, revision=rev, repo_type=repo_type)
    copyfile(cached, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--all", action="store_true", help="also fetch the two secondary datasets")
    args = parser.parse_args()
    lb = "nebius/SWE-rebench-leaderboard-trajectories"
    for shard in sorted(HfApi().list_repo_files(lb, repo_type="dataset", revision=REV_LB)):
        if shard.startswith("data/python_spring2026/") and shard.endswith(".parquet"):
            fetch(lb, REV_LB, shard, "lb/" + Path(shard).name)
    if args.all:
        fetch("SWE-bench/SWE-smith-trajectories", REV_SMITH, "data/tool-00000-of-00008.parquet", "tool-00000.parquet")
        fetch("nebius/SWE-rebench-openhands-trajectories", REV_OH, "trajectories.parquet", "rebench-traj.parquet")
        for part in ("test-00000-of-00002", "test-00001-of-00002", "filtered-00000-of-00001"):
            fetch("nebius/SWE-rebench", REV_RB_META, f"data/{part}.parquet", f"rebench-meta-{part}.parquet")
    fetch("Qwen/Qwen3-8B", "main", "tokenizer.json", "qwen3_tokenizer.json", repo_type="model")
