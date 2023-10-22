compile:
	git submodule update --init --recursive
	cargo build --manifest-path Code/job_system/Cargo.toml